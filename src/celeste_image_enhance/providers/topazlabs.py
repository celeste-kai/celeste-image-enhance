"""Topaz Labs image enhancement provider."""

import asyncio
import io
from typing import Any, Literal

import aiohttp
from celeste_core import ImageArtifact, Provider
from celeste_core.base.image_enhancer import BaseImageEnhancer
from celeste_core.config.settings import settings

EnhancementType = Literal["enhance", "sharpen", "denoise"]


class TopazLabsImageEnhancer(BaseImageEnhancer):
    """Topaz Labs image enhancement client."""

    def __init__(self, model: str = "Standard V2", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.model_name = model
        self.api_key = settings.topazlabs.api_key
        self.base_url = "https://api.topazlabs.com/image/v1"

    async def enhance_image(
        self,
        image: ImageArtifact,
        enhancement_type: EnhancementType = "enhance",
        scale_factor: int = 2,
        **kwargs: Any,
    ) -> ImageArtifact:
        """Enhance an image using Topaz Labs API."""
        headers = {"X-API-Key": self.api_key}

        # Prepare form data
        data = aiohttp.FormData()
        data.add_field("model", self.model_name)
        data.add_field("scale", str(scale_factor))
        data.add_field(
            "image",
            io.BytesIO(image.data),
            filename="image.jpg",
            content_type="image/jpeg",
        )

        async with aiohttp.ClientSession() as session:
            # Submit request
            async with session.post(
                f"{self.base_url}/{enhancement_type}/async", headers=headers, data=data
            ) as response:
                job_id = (await response.json())["process_id"]

            # Poll for completion
            while True:
                async with session.get(
                    f"{self.base_url}/status/{job_id}", headers=headers
                ) as response:
                    status_result = await response.json()
                    if status_result["status"] == "Completed":
                        break
                    await asyncio.sleep(2)

            # Get download URL and fetch image
            async with session.get(
                f"{self.base_url}/download/{job_id}", headers=headers
            ) as response:
                download_info = await response.json()
                image_url = download_info["download_url"]

            async with session.get(image_url) as response:
                enhanced_data = await response.read()

        return ImageArtifact(
            data=enhanced_data,
            metadata={
                "provider": Provider.TOPAZLABS,
                "model": self.model_name,
                "enhancement_type": enhancement_type,
            },
        )
