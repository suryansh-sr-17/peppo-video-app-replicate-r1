import os
import logging
from typing import Dict, Optional
import replicate
from replicate.exceptions import ModelError
from dotenv import load_dotenv
from .base import BaseProvider, VideoJob

# Load environment variables
load_dotenv()

class ReplicateProvider(BaseProvider):
    """
    Replicate provider for text-to-video generation.
    Uses Replicate's API to generate videos from text prompts.
    """

    def __init__(self, api_token: Optional[str] = None, model: Optional[str] = None):
        self.api_token = api_token or os.getenv("REPLICATE_API_TOKEN")
        # Using a cost-effective text-to-video model - this can be configured via env
        # Default to verified working text-to-video model
        self.model = model or os.getenv("REPLICATE_MODEL", "pixverse/pixverse-v5")
        self._predictions: Dict[str, Dict] = {}  # Cache predictions
        self.log = logging.getLogger("provider.replicate")
        
        if not self.api_token:
            self.log.warning("No REPLICATE_API_TOKEN found. Provider may not work correctly.")

    def submit(self, prompt: str, options: Dict) -> VideoJob:
        """
        Submit a text-to-video generation request to Replicate.
        """
        try:
            # Set up the API token
            if self.api_token:
                os.environ["REPLICATE_API_TOKEN"] = self.api_token

            # Prepare input for the model (Pixverse parameters)
            model_input = {
                "prompt": prompt,
                "aspect_ratio": "16:9",
                "duration": 5
            }
            
            # Apply style-based overrides if provided
            if options and options.get("style"):
                style_overrides = self._get_style_overrides(options["style"])
                model_input.update(style_overrides)

            # Create prediction using async mode (non-blocking)
            prediction = replicate.predictions.create(
                model=self.model,
                input=model_input
            )

            # Cache the prediction for later fetching
            self._predictions[prediction.id] = {
                "prediction": prediction,
                "status": prediction.status,
                "output": None
            }

            self.log.info(f"Created Replicate prediction: {prediction.id}")
            return VideoJob(job_id=prediction.id, status="processing")

        except ModelError as e:
            self.log.error(f"Replicate model error: {e}")
            return VideoJob(job_id="n/a", status="failed", error=f"Model error: {str(e)}")
        except Exception as e:
            self.log.exception("Error submitting job to Replicate")
            return VideoJob(job_id="n/a", status="failed", error=str(e))

    def fetch(self, job_id: str) -> VideoJob:
        """
        Check the status of a Replicate prediction and return updated VideoJob.
        """
        try:
            # Set up the API token
            if self.api_token:
                os.environ["REPLICATE_API_TOKEN"] = self.api_token

            cached = self._predictions.get(job_id)
            if not cached:
                # Try to get prediction from Replicate directly
                try:
                    prediction = replicate.predictions.get(job_id)
                    cached = {
                        "prediction": prediction,
                        "status": prediction.status,
                        "output": prediction.output
                    }
                    self._predictions[job_id] = cached
                except Exception:
                    return VideoJob(job_id, status="not_found", error="Unknown job")

            prediction = cached["prediction"]
            
            # Refresh prediction status
            prediction.reload()
            
            # Map Replicate status to our status
            status = self._map_status(prediction.status)
            
            # Update cache
            cached["status"] = prediction.status
            cached["output"] = prediction.output

            if status == "succeeded" and prediction.output:
                # Replicate returns the video URL directly
                video_url = prediction.output
                if isinstance(video_url, list) and len(video_url) > 0:
                    video_url = video_url[0]
                
                # Convert FileOutput to URL if needed
                if hasattr(video_url, 'url'):
                    video_url = video_url.url
                
                return VideoJob(job_id=job_id, status="succeeded", video_url=str(video_url))
            
            elif status == "failed":
                error_msg = getattr(prediction, 'error', 'Generation failed')
                return VideoJob(job_id=job_id, status="failed", error=str(error_msg))
            
            else:
                return VideoJob(job_id=job_id, status=status)

        except Exception as e:
            self.log.exception("Error fetching job result from Replicate")
            return VideoJob(job_id, status="failed", error=str(e))

    def _map_status(self, replicate_status: str) -> str:
        """Map Replicate prediction status to our VideoJob status."""
        status_map = {
            "starting": "processing",
            "processing": "processing",
            "succeeded": "succeeded",
            "failed": "failed",
            "canceled": "failed"
        }
        return status_map.get(replicate_status, "processing")

    def _get_style_overrides(self, style: str) -> Dict:
        """Get style-specific parameter overrides."""
        style = style.lower()
        
        if style == "cinematic":
            return {
                "duration": 8,
                "aspect_ratio": "16:9"
            }
        elif style == "anime":
            return {
                "duration": 5,
                "aspect_ratio": "16:9"
            }
        elif style == "product":
            return {
                "duration": 5,
                "aspect_ratio": "1:1"
            }
        
        return {}