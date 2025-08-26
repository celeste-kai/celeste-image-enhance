# celeste-image-enhance

Image enhancement across providers for the Celeste ecosystem, starting with Topaz Labs.

## Features

- **Image Upscaling**: Scale images up to 16x with AI-powered enhancement
- **Denoising**: Remove sensor noise and grain from images
- **Sharpening**: Bring blurred images into focus
- **Face Recovery**: Enhance facial details in portraits
- **Multiple Models**: Choose from Standard V2, Low Resolution V2, CGI, High Fidelity V2, and Text Refine

## Supported Providers

- **Topaz Labs**: Industry-leading AI upscaling and enhancement

## Quick Start

```python
from celeste_image_enhance import create_image_enhancer
from celeste_core import ImageArtifact, Provider

# Create enhancer
enhancer = create_image_enhancer(Provider.TOPAZLABS, model="standard-v2")

# Load image
image = ImageArtifact(data=open("input.jpg", "rb").read())

# Enhance image
result = await enhancer.enhance_image(
    image,
    scale_factor=4,
    enhancement_type="upscale"
)

# Save result
with open("output.jpg", "wb") as f:
    f.write(result.data)
```

## Installation

```bash
cd celeste-image-enhance
uv add -e .
```