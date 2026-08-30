from typing import Dict, Any, List
from app.services.providers.base_provider import BaseBlockchainProvider

class DemoDataProvider(BaseBlockchainProvider):
    async def get_address(self, address: str) -> Dict[str, Any]:
        return {
            "address": address,
            "chain_stats": {
                "funded_txo_count": 12,
                "funded_txo_sum": 2450000000, # satoshis (24.5 BTC)
                "spent_txo_count": 10,
                "spent_txo_sum": 2000000000,  # satoshis (20.0 BTC)
                "tx_count": 22
            },
            "mempool_stats": {
                "funded_txo_count": 0,
                "funded_txo_sum": 0,
                "spent_txo_count": 0,
                "spent_txo_sum": 0,
                "tx_count": 0
            },
            "source": "Demo Mode (SIH26146)"
        }

    async def get_transaction(self, txid: str) -> Dict[str, Any]:
        return {
            "txid": txid,
            "version": 2,
            "locktime": 0,
            "vin": [
                {
                    "txid": "prev_tx_hash_001",
                    "vout": 0,
                    "prevout": {
                        "scriptpubkey_address": "bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0",
                        "value": 1500000000
                    }
                }
            ],
            "vout": [
                {
                    "scriptpubkey_address": "bc1qrapid83k92m1n0v9c8x7z6543210forward",
                    "value": 1450000000
                },
                {
                    "scriptpubkey_address": "bc1qchange9876543210residual000111222",
                    "value": 4900000
                }
            ],
            "size": 225,
            "weight": 561,
            "fee": 100000,
            "status": {
                "confirmed": True,
                "block_height": 840000,
                "block_hash": "000000000000000000021a8c8e9b0c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b",
                "block_time": 1724745600
            },
            "source": "Demo Mode (SIH26146)"
        }

    async def get_address_transactions(self, address: str, limit: int = 20) -> List[Dict[str, Any]]:
        demo_tx = await self.get_transaction("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
        return [demo_tx]
