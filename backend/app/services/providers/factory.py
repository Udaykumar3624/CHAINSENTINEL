from app.core.config import settings
from app.services.providers.base_provider import BaseBlockchainProvider
from app.services.providers.demo_provider import DemoDataProvider
from app.services.providers.mempool_provider import MempoolSpaceProvider

def get_blockchain_provider(force_live: Optional[bool] = None) -> BaseBlockchainProvider:
    """
    Returns MempoolSpaceProvider if LIVE_DATA_ENABLED is True or force_live is True.
    Otherwise returns DemoDataProvider.
    """
    use_live = settings.LIVE_DATA_ENABLED if force_live is None else force_live
    if use_live:
        return MempoolSpaceProvider(
            base_url=settings.MEMPOOL_API_URL,
            timeout_seconds=float(settings.REQUEST_TIMEOUT_SECONDS)
        )
    return DemoDataProvider()
