import os
import ipaddress
import logging
from typing import Optional, Dict, Any
from functools import lru_cache

logger = logging.getLogger("chainsentinel.geoip")

GEOIP_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "geoip"))

# Fallback prefix mappings for well-known networks when MMDB is missing or offline
FALLBACK_PREFIXES = [
    ("8.8.8.0/24", "United States", "US", "AS15169", "Google LLC"),
    ("8.8.4.0/24", "United States", "US", "AS15169", "Google LLC"),
    ("1.1.1.0/24", "Australia", "AU", "AS13335", "Cloudflare, Inc."),
    ("1.0.0.0/24", "Australia", "AU", "AS13335", "Cloudflare, Inc."),
    ("13.225.0.0/16", "India", "IN", "AS16509", "Amazon.com, Inc."),
    ("13.232.0.0/15", "India", "IN", "AS16509", "Amazon.com, Inc."),
    ("185.220.101.0/24", "Germany", "DE", "AS60729", "Stiftung Erneuerbare Freiheit"),
    ("198.51.100.0/24", "United States", "US", "AS64500", "Demo Financial Services AS"),
    ("203.0.113.0/24", "Singapore", "SG", "AS64501", "Demo Asia Exchange Network"),
    ("52.84.0.0/15", "United Kingdom", "GB", "AS16509", "Amazon.com, Inc."),
    ("133.242.0.0/16", "Japan", "JP", "AS9370", "SAKURA Internet Inc."),
    ("193.134.0.0/16", "Switzerland", "CH", "AS13030", "Init7 (Switzerland) Ltd."),
]

class GeoIPService:
    def __init__(self):
        self._country_reader = None
        self._asn_reader = None
        self._initialized = False
        self._fallback_subnets = []
        for cidr, c_name, c_code, asn, asn_org in FALLBACK_PREFIXES:
            try:
                self._fallback_subnets.append((ipaddress.ip_network(cidr), c_name, c_code, asn, asn_org))
            except Exception:
                pass
        self._init_readers()

    def _init_readers(self):
        if self._initialized:
            return
        try:
            import maxminddb
            country_path = os.path.join(GEOIP_DATA_DIR, "dbip-country-lite.mmdb")
            asn_path = os.path.join(GEOIP_DATA_DIR, "dbip-asn-lite.mmdb")

            if os.path.exists(country_path):
                try:
                    self._country_reader = maxminddb.open_database(country_path)
                    logger.info(f"Loaded Country Geo-IP database from {country_path}")
                except Exception as e:
                    logger.warning(f"Could not open Country Geo-IP database: {e}")

            if os.path.exists(asn_path):
                try:
                    self._asn_reader = maxminddb.open_database(asn_path)
                    logger.info(f"Loaded ASN Geo-IP database from {asn_path}")
                except Exception as e:
                    logger.warning(f"Could not open ASN Geo-IP database: {e}")

            self._initialized = True
        except ImportError:
            logger.info("maxminddb not installed, using fallback GeoIP resolution.")

    @lru_cache(maxsize=10000)
    def resolve_ip(self, ip_str: Optional[str]) -> Dict[str, Any]:
        """Resolves an IPv4 or IPv6 string to geographic and ASN context safely."""
        if not ip_str or not isinstance(ip_str, str):
            return {
                "ip": "Unknown",
                "is_valid": False,
                "is_private": False,
                "country": "Unknown",
                "country_code": "UNKNOWN",
                "asn": "Unknown",
                "asn_org": "Unknown"
            }

        cleaned_ip = ip_str.strip()
        try:
            ip_obj = ipaddress.ip_address(cleaned_ip)
        except ValueError:
            return {
                "ip": cleaned_ip,
                "is_valid": False,
                "is_private": False,
                "country": "Unknown",
                "country_code": "UNKNOWN",
                "asn": "Unknown",
                "asn_org": "Unknown"
            }

        # Check for Private, Loopback, or Reserved IPs
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved or ip_obj.is_link_local:
            return {
                "ip": cleaned_ip,
                "is_valid": True,
                "is_private": True,
                "country": "Private Network",
                "country_code": "PRIVATE",
                "asn": "AS0",
                "asn_org": "Local / RFC1918 Network"
            }

        # Query Country MMDB if open
        country_name = "Unknown"
        country_code = "UNKNOWN"
        if self._country_reader:
            try:
                res = self._country_reader.get(cleaned_ip)
                if res and isinstance(res, dict):
                    country_data = res.get("country", {}) or res.get("registered_country", {})
                    country_name = country_data.get("names", {}).get("en") or res.get("continent", {}).get("names", {}).get("en") or "Unknown"
                    country_code = country_data.get("iso_code") or "UNKNOWN"
            except Exception:
                pass

        # Query ASN MMDB if open
        asn_str = "Unknown"
        asn_org = "Unknown"
        if self._asn_reader:
            try:
                res = self._asn_reader.get(cleaned_ip)
                if res and isinstance(res, dict):
                    asn_num = res.get("autonomous_system_number")
                    if asn_num:
                        asn_str = f"AS{asn_num}"
                    asn_org = res.get("autonomous_system_organization") or "Unknown"
            except Exception:
                pass

        # Use fallback prefixes if either country or ASN is unknown
        if country_name == "Unknown" or asn_str == "Unknown":
            for net, f_country, f_code, f_asn, f_org in self._fallback_subnets:
                if ip_obj in net:
                    if country_name == "Unknown":
                        country_name = f_country
                        country_code = f_code
                    if asn_str == "Unknown":
                        asn_str = f_asn
                        asn_org = f_org
                    break

        return {
            "ip": cleaned_ip,
            "is_valid": True,
            "is_private": False,
            "country": country_name,
            "country_code": country_code,
            "asn": asn_str,
            "asn_org": asn_org
        }

    def resolve_pair(self, src_ip: Optional[str], dst_ip: Optional[str]) -> Dict[str, Any]:
        """Resolves both source and destination IPs into a structured network context."""
        src_res = self.resolve_ip(src_ip)
        dst_res = self.resolve_ip(dst_ip)
        return {
            "source_ip": src_res["ip"],
            "source_country": src_res["country"],
            "source_country_code": src_res["country_code"],
            "source_asn": src_res["asn"],
            "source_asn_org": src_res["asn_org"],
            "source_is_private": src_res["is_private"],
            "destination_ip": dst_res["ip"],
            "destination_country": dst_res["country"],
            "destination_country_code": dst_res["country_code"],
            "destination_asn": dst_res["asn"],
            "destination_asn_org": dst_res["asn_org"],
            "destination_is_private": dst_res["is_private"],
            "disclaimer": (
                "Geo-IP information is contextual telemetry and may be approximate. "
                "It is not proof of physical location, citizenship, or legal guilt."
            )
        }

    def enrich_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Enriches a transaction dictionary with Geo-IP and ASN metadata."""
        src_ip = record.get("src_ip")
        dst_ip = record.get("dst_ip")
        
        pair = self.resolve_pair(src_ip, dst_ip)
        
        # Preserve existing non-empty geo_country/asn unless empty or 'Unknown'
        if not record.get("geo_country") or record.get("geo_country") in ["Unknown", "unknown", ""]:
            record["geo_country"] = pair["source_country"] if pair["source_country"] != "Unknown" else pair["destination_country"]
        
        if not record.get("asn") or record.get("asn") in ["Unknown", "unknown", ""]:
            record["asn"] = pair["source_asn"] if pair["source_asn"] != "Unknown" else pair["destination_asn"]

        record["src_country"] = pair["source_country"]
        record["src_country_code"] = pair["source_country_code"]
        record["src_asn"] = pair["source_asn"]
        record["src_asn_org"] = pair["source_asn_org"]

        record["dst_country"] = pair["destination_country"]
        record["dst_country_code"] = pair["destination_country_code"]
        record["dst_asn"] = pair["destination_asn"]
        record["dst_asn_org"] = pair["destination_asn_org"]

        record["network_context"] = pair
        return record

    def resolve(self, ip_str: Optional[str]) -> Dict[str, Any]:
        """Alias for resolve_ip."""
        return self.resolve_ip(ip_str)

# Singleton instance
geoip_service = GeoIPService()
