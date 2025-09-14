# Test Scripts

This folder contains utility scripts used during development and testing of the Replicate API integration.

## Scripts Overview

### Core Testing Scripts
- **`test_env_loading.py`** - Verifies environment variables are loaded correctly and tests API connections
- **`test_prompt_optimizer.py`** - Tests the OpenAI prompt optimization feature
- **`test_video_generation.py`** - Tests video generation with Replicate API and ReplicateProvider

### Model Discovery Scripts
- **`test_replicate_models.py`** - Tests specific text-to-video models for availability
- **`find_working_video_model.py`** - Searches for working text-to-video models
- **`search_video_models.py`** - Comprehensive search for video-related models on Replicate

## Usage

Make sure you have your API keys set in the `.env` file before running any tests:

```bash
# Run from the project root directory
python test_scripts/test_env_loading.py
python test_scripts/test_video_generation.py
```

## Requirements

These scripts require the same dependencies as the main application:
- `replicate`
- `openai` 
- `python-dotenv`

## Note

These scripts were used during the development process to debug and verify the integration. They are kept for reference and future debugging purposes.