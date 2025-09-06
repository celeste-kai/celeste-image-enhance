from importlib import import_module
from typing import Any

from celeste_core import Provider
from celeste_core.base.image_enhancer import BaseImageEnhancer
from celeste_core.config.settings import settings

from .mapping import PROVIDER_MAPPING

__version__ = "0.1.0"


def create_image_enhancer(provider: Provider | str, **kwargs: Any) -> BaseImageEnhancer:
    prov = Provider(provider) if isinstance(provider, str) else provider
    if prov not in PROVIDER_MAPPING:
        raise ValueError(f"Provider '{prov.value}' is not wired for image enhancement.")

    settings.validate_for_provider(prov.value)
    module_path, class_name = PROVIDER_MAPPING[prov]
    module = import_module(f"celeste_image_enhance{module_path}")
    return getattr(module, class_name)(**kwargs)


__all__ = ["create_image_enhancer", "BaseImageEnhancer"]
