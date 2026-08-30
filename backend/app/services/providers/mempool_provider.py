import re
import asyncio
import httpx
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status
from app.services.providers.base_provider import BaseBlockchainProvider
from app.core.logging import logger

BTC_ADDRESS_REGEX = re.compile(r"^(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-Z0-9]{11,87}|tb1[a-zA-Z0-9]{11,87})$", re.IGNORECASE)
BTC_TXID_REGEX = re.compile(r"^[a-fA-F0-9]{64}$")

class MempoolSpaceProvider(BaseBlockchainProvider):
    def __init__(self, base_url: str = "https://mempool.space/api", timeout_seconds: float = 5.0, max_retries: int = 2):
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

    def validate_address(self, address: str):
        if not address or not BTC_ADDRESS_REGEX.match(address.strip()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid Bitcoin address format '{address}'. Address must be Legacy (1...), P2SH (3...), SegWit (bc1q...), or Taproot (bc1p...)."
            )

    def validate_txid(self, txid: str):
        if not txid or not BTC_TXID_REGEX.match(txid.strip()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid Bitcoin transaction ID format '{txid}'. Must be a 64-character hex TxID."
            )

    async def get_address(self, address: str) -> Dict[str, Any]:
        self.validate_address(address)
        url = f"{self.base_url}/address/{address.strip()}"
        data = await self._make_request(url)
        data["source"] = "Live Mempool.space API"
        return data

    async def get_transaction(self, txid: str) -> Dict[str, Any]:
        self.validate_txid(txid)
        url = f"{self.base_url}/tx/{txid.strip()}"
        data = await self._make_request(url)
        data["source"] = "Live Mempool.space API"
        return data

    async def get_address_transactions(self, address: str, limit: int = 20) -> List[Dict[str, Any]]:
        self.validate_address(address)
        url = f"{self.base_url}/address/{address.strip()}/txs"
        data = await self._make_request(url)
        if isinstance(data, list):
            return data[:limit]
        return []

    async def _make_request(self, url: str) -> Any:
        delay = 0.5
        for attempt in range(1, self.max_retries + 2):
            try:
                async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                    response = await client.get(url)
                    if response.status_code == 200:
                        return response.json()
                    elif response.status_code == 404:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Requested Bitcoin entity not found on live network (HTTP 404)."
                        )
                    elif response.status_code == 429:
                        raise HTTPException(
                            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="Live Mempool.space API rate limit reached (HTTP 429). Please retry later or switch to Demo Mode."
                        )
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_502_BAD_GATEWAY,
                            detail=f"Live Mempool.space API error (HTTP {response.status_code})."
                        )
            except httpx.TimeoutException:
                logger.warning(f"Mempool.space request timeout (attempt {attempt}/{self.max_retries + 1}) for {url}")
                if attempt > self.max_retries:
                    raise HTTPException(
                        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                        detail="Live Mempool.space API request timed out. Please check internet connection or switch to Demo Mode."
                    )
            except httpx.RequestError as exc:
                logger.error(f"Mempool.space connection error on {url}: {exc}")
                if attempt > self.max_retries:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Unable to reach live Mempool.space API network. Please switch to Demo Mode."
                    )

            await asyncio.sleep(delay)
            delay *= 2
