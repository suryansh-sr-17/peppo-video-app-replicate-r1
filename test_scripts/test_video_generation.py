#!/usr/bin/env python3
"""
Test video generation with Replicate API directly
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🧪 Testing Video Generation with Replicate...")
print("=" * 50)

# Test direct Replicate API call
try:
    import replicate
    
    replicate_token = os.getenv("REPLICATE_API_TOKEN")
    model = os.getenv("REPLICATE_MODEL")
    
    print(f"API Token: {replicate_token[:10]}...{replicate_token[-4:]}")
    print(f"Model: {model}")
    
    if replicate_token:
        os.environ["REPLICATE_API_TOKEN"] = replicate_token
        
        print("\n🎬 Creating prediction...")
        
        # Test with the current model
        prediction = replicate.predictions.create(
            model=model,
            input={
                "prompt": "A robot fighting an ant",
                "aspect_ratio": "16:9",
                "duration": 5
            }
        )
        
        print(f"✅ Prediction created!")
        print(f"   ID: {prediction.id}")
        print(f"   Status: {prediction.status}")
        print(f"   Model: {prediction.model}")
        
        # Check status a few times
        import time
        for i in range(3):
            prediction.reload()
            print(f"   Status check {i+1}: {prediction.status}")
            if prediction.status in ["succeeded", "failed"]:
                break
            time.sleep(2)
        
        if prediction.status == "succeeded":
            print(f"✅ Video generated successfully!")
            print(f"   Output: {prediction.output}")
        elif prediction.status == "failed":
            print(f"❌ Generation failed: {prediction.error}")
        else:
            print(f"⏳ Still processing: {prediction.status}")
            
    else:
        print("❌ No Replicate API token found")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)

# Test our provider
print("🧪 Testing ReplicateProvider...")
try:
    from app.providers.replicate import ReplicateProvider
    
    provider = ReplicateProvider()
    print(f"Provider initialized with model: {provider.model}")
    
    # Test submit
    job = provider.submit("A robot fighting an ant", {"style": "anime"})
    print(f"Job submitted: {job.job_id}, Status: {job.status}")
    
    if job.status != "failed":
        # Test fetch
        import time
        for i in range(3):
            result = provider.fetch(job.job_id)
            print(f"Fetch {i+1}: Status = {result.status}")
            if result.status in ["succeeded", "failed"]:
                if result.status == "succeeded":
                    print(f"✅ Video URL: {result.video_url}")
                else:
                    print(f"❌ Error: {result.error}")
                break
            time.sleep(2)
    else:
        print(f"❌ Job failed: {job.error}")
        
except Exception as e:
    print(f"❌ Provider error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n🎯 Test Complete!")