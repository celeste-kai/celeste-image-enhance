from celeste_core.enums.capability import Capability
from celeste_core.enums.providers import Provider

# Capability for this domain package
CAPABILITY: Capability = Capability.IMAGE_ENHANCE

# Provider wiring for image enhancement clients
PROVIDER_MAPPING: dict[Provider, tuple[str, str]] = {
    Provider.TOPAZLABS: (".providers.topazlabs", "TopazLabsImageEnhancer"),
}

__all__ = ["CAPABILITY", "PROVIDER_MAPPING"]
