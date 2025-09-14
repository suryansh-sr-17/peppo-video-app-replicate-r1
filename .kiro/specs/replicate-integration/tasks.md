# Implementation Plan

- [x] 1. Add Replicate dependency to project

  - Add `replicate` package to requirements.txt
  - _Requirements: 3.2_

- [x] 2. Create Replicate provider implementation

  - [x] 2.1 Research and identify cheapest text-to-video model on Replicate

    - Search Replicate model catalog for cost-effective text-to-video models
    - Document the selected model identifier and pricing
    - _Requirements: 1.1_

  - [x] 2.2 Implement ReplicateProvider class

    - Create `app/providers/replicate.py` with ReplicateProvider class
    - Implement `submit()` method to create Replicate predictions
    - Implement `fetch()` method to check prediction status
    - Handle Replicate API authentication with REPLICATE_API_TOKEN
    - Map Replicate prediction statuses to VideoJob statuses
    - _Requirements: 1.1, 1.2, 1.3_

- [x] 3. Update video generator to use Replicate provider

  - [x] 3.1 Modify provider factory in video_generator.py

    - Update `_build_provider()` function to default to ReplicateProvider
    - Add support for "replicate" provider name
    - _Requirements: 2.1, 3.3_

- [x] 4. Update environment configuration

  - [x] 4.1 Update .env file for Replicate integration

    - Set VIDEO_PROVIDER to "replicate" by default
    - Add REPLICATE_API_TOKEN placeholder
    - Add REPLICATE_MODEL configuration
    - _Requirements: 1.1, 3.3_

- [x] 5. Handle video file streaming from Replicate

  - [x] 5.1 Update video endpoint to handle Replicate FileOutput


    - Modify `/video/{job_id}` endpoint to stream from Replicate URLs when available
    - Ensure proper video streaming with range requests support
    - Maintain fallback to placeholder.mp4 for failed generations
    - _Requirements: 1.4, 1.5, 2.2_

- [ ] 6. Test integration with actual API key
  - [ ] 6.1 Test video generation pipeline end-to-end
    - Submit test prompts and verify video generation works
    - Test video playback in web frontend
    - Verify error handling for failed generations
    - Test job caching mechanism with real Replicate responses
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3_
