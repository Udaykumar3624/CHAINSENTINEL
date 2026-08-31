import pytest
from app.services.geoip import geoip_service
from app.services.dataset.parser import UniversalDatasetParser

def test_geoip_service_resolution():
    # 1. Public IP Google DNS
    res_google = geoip_service.resolve("8.8.8.8")
    assert res_google["country"] == "United States"
    assert res_google["country_code"] == "US"
    assert "15169" in res_google["asn"]

    # 2. Public IP Cloudflare DNS
    res_cf = geoip_service.resolve("1.1.1.1")
    assert "AS13335" in res_cf["asn"] or "Cloudflare" in res_cf["asn_org"] or res_cf["country"] != "Unknown"

    # 3. Private IP RFC1918
    res_private = geoip_service.resolve("192.168.1.100")
    assert res_private["country"] == "Private Network"
    assert res_private["country_code"] == "PRIVATE"
    assert res_private["is_private"] is True

    # 4. Local loopback
    res_local = geoip_service.resolve("127.0.0.1")
    assert res_local["is_private"] is True

    # 5. Pair resolution
    pair = geoip_service.resolve_pair("8.8.8.8", "185.220.101.5")
    assert pair["source_country"] == "United States"
    assert "Germany" in pair["destination_country"] or "DE" in pair["destination_country_code"]

def test_dataset_parser_with_network_fields():
    csv_content = """transaction_id,timestamp,src_ip,dst_ip,src_port,dst_port,input_address,output_address,amount_btc,scenario,label
tx_sih_001,2026-08-30T10:00:00Z,8.8.8.8,185.220.101.5,51234,8333,bc1qsender001,bc1qrecv002,1.2500,rapid_forwarding,suspicious
"""
    result = UniversalDatasetParser.parse_content(csv_content, "sih_test.csv")
    assert result.is_valid is True
    assert len(result.normalized_transactions) == 1
    tx = result.normalized_transactions[0]
    assert tx.src_ip == "8.8.8.8"
    assert tx.dst_ip == "185.220.101.5"
    assert tx.src_port == 51234
    assert tx.dst_port == 8333
    assert tx.geo_country == "United States"
    assert "15169" in str(tx.asn)
