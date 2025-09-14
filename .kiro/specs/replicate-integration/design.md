# Design Document

## Overview

The integration will replace the current ModelsLab provider with a new Replicate provider that implements the existing BaseProvider interface. Replicate will be the default and primary provider for the project. This approach ensures minimal changes to the existing codebase while enabling real video generation capabilities.

## Architecture

The current provider-based architecture is well-suited for this integration:

```
FastAPI App -> VideoGenerator -> BaseProvider -> ReplicateProvider
```

The VideoGenerator service will continue to work unchanged, as it depends only on the BaseProvider interface.

## Components and Interfaces

### ReplicateProvider Class

A new provider class that implements the BaseProvider interface:

```python
class ReplicateProvider(BaseProvider):
    def submit(self, prompt: str, options: Dict) -> VideoJob
    def fetch(self, job_id: str) -> VideoJob
```

### Key Integration Points

1. **Model Selection**: Use a cost-effective text-to-video model from Replicate's catalog
2. **API Authentication**: Use REPLICATE_API_TOKEN environment variable
3. **Job Management**: Map Replicate prediction IDs to our VideoJob objects
4. **File Handling**: Handle Replicate's FileOutput objects for video files

## Data Models

### Environment Variables
- `REPLICATE_API_TOKEN`: API key for Replicate authentication (primary and default provider)
- `VIDEO_PROVIDER`: Defaults to "replicate" as the primary provider
- `REPLICATE_MODEL`: Model identifier for text-to-video generation

### VideoJob Mapping
- `job_id`: Maps to Replicate prediction ID
- `status`: Maps Replicate prediction status to our status format
- `video_url`: Points to generated video file or streaming endpoint

## Error Handling

### API Errors
- Network failures: Return VideoJob with "failed" status and error message
- Authentication errors: Log and return appropriate error response
- Model errors: Parse Replicate error messages and return user-friendly errors

### File Handling Errors
- Video download failures: Retry mechanism with fallback to error state
- File format issues: Validate and convert if necessary

## Testing Strategy

### Development Testing
1. Use Replicate's cheapest text-to-video model for cost-effective testing
2. Implement mock responses for unit tests
3. Test error scenarios with invalid inputs

### Integration Testing
1. Test full pipeline from prompt submission to video playback
2. Verify video files are properly served through existing `/video/{job_id}` endpoint
3. Test caching mechanism with Replicate-generated content

## Implementation Details

### Model Selection Research
Based on Replicate's catalog, we'll identify the most cost-effective text-to-video model that provides reasonable quality for development and testing.

### File Management
- Replicate returns FileOutput objects that can be streamed directly
- Videos will be served through the existing video streaming endpoint
- No local file storage required - stream directly from Replicate's URLs

### Status Mapping
```
Replicate Status -> Our Status
"starting" -> "processing"
"processing" -> "processing" 
"succeeded" -> "succeeded"
"failed" -> "failed"
"canceled" -> "failed"
```

### Dependencies
- Add `replicate` package to requirements.txt
- No other external dependencies required