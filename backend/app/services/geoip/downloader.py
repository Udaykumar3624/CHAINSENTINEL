import os
import gzip
import shutil
import urllib.request
import logging

logger = logging.getLogger("chainsentinel.geoip.downloader")

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "geoip"))

DBIP_COUNTRY_URL = "https://download.db-ip.com/free/dbip-country-lite-2026-08.mmdb.gz"
DBIP_ASN_URL = "https://download.db-ip.com/free/dbip-asn-lite-2026-08.mmdb.gz"

def ensure_geoip_databases():
    os.makedirs(DATA_DIR, exist_ok=True)
    country_mmdb = os.path.join(DATA_DIR, "dbip-country-lite.mmdb")
    asn_mmdb = os.path.join(DATA_DIR, "dbip-asn-lite.mmdb")

    if not os.path.exists(country_mmdb):
        try:
            logger.info("Downloading DB-IP Country Lite database...")
            gz_path = country_mmdb + ".gz"
            urllib.request.urlretrieve(DBIP_COUNTRY_URL, gz_path)
            with gzip.open(gz_path, 'rb') as f_in:
                with open(country_mmdb, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            if os.path.exists(gz_path): os.remove(gz_path)
        except Exception as e:
            logger.warning(f"Could not download country mmdb: {e}")

    if not os.path.exists(asn_mmdb):
        try:
            logger.info("Downloading DB-IP ASN Lite database...")
            gz_path = asn_mmdb + ".gz"
            urllib.request.urlretrieve(DBIP_ASN_URL, gz_path)
            with gzip.open(gz_path, 'rb') as f_in:
                with open(asn_mmdb, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            if os.path.exists(gz_path): os.remove(gz_path)
        except Exception as e:
            logger.warning(f"Could not download ASN mmdb: {e}")

if __name__ == "__main__":
    ensure_geoip_databases()
