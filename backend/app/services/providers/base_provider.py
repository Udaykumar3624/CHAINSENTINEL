from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseBlockchainProvider(ABC):
    @abstractmethod
    async def get_address(self, address: str) -> Dict[str, Any]:
        """Fetch address summary and stats."""
        pass

    @abstractmethod
    async def get_transaction(self, txid: str) -> Dict[str, Any]:
        """Fetch transaction details."""
        pass

    @abstractmethod
    async def get_address_transactions(self, address: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch recent transaction history for an address."""
        pass
