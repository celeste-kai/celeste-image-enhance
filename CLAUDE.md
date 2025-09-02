# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Celeste-image-enhance is a Python package providing AI-powered image enhancement capabilities through multiple providers, starting with Topaz Labs. It's part of the larger Celeste ecosystem for multimodal AI.

## Architecture

### Package Structure
- **src/celeste_image_enhance/**: Main package following src/ layout
  - `__init__.py`: Factory function `create_image_enhancer()` 
  - `mapping.py`: Provider-to-implementation mapping using PROVIDER_MAPPING dict
  - `providers/`: Provider implementations (currently TopazLabs)

### Key Components
- **BaseImageEnhancer**: Abstract base class from celeste-core defining the interface
- **TopazLabsImageEnhancer**: Async implementation using aiohttp for API calls
- **Provider mapping system**: Links Provider enum to implementation classes
- **Factory pattern**: `create_image_enhancer()` creates instances based on provider

### Dependencies
- **celeste-core**: Base classes, enums, ImageArtifact, settings management
- **aiohttp**: Async HTTP client for API calls
- **Pillow**: Image processing utilities
- **streamlit**: Interactive demo application

## Development Commands

### Package Installation
```bash
uv add -e .                    # Install in editable mode for development
```

### Code Quality
```bash
ruff check                     # Lint Python code
ruff check --fix              # Auto-fix linting issues
ruff format                    # Format Python code
mypy src/                      # Type checking
```

### Pre-commit Hooks
```bash
pre-commit install             # Install pre-commit hooks
pre-commit run --all-files     # Run all hooks manually
```

### Demo Application
```bash
streamlit run example.py       # Run interactive Streamlit demo
```

## Key Patterns

### Adding New Providers
1. Add provider to PROVIDER_MAPPING in `mapping.py`
2. Create new provider class in `providers/` inheriting from BaseImageEnhancer
3. Implement required `enhance_image()` async method
4. Follow existing pattern for API authentication and error handling

### Provider Implementation Requirements
- Inherit from `BaseImageEnhancer` 
- Implement async `enhance_image()` method
- Use `ImageArtifact` for input/output with metadata
- Handle authentication through celeste-core settings
- Use aiohttp for async HTTP operations
- Include provider info in returned metadata

### API Integration Pattern
The TopazLabs implementation demonstrates the async workflow:
1. Submit job with form data (image + parameters)
2. Poll status endpoint until completion
3. Download result from provided URL
4. Return ImageArtifact with enhanced data and metadata