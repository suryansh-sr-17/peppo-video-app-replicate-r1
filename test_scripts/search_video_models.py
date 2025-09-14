#!/usr/bin/env python3
"""
Search for available text-to-video models on Replicate
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import replicate

replicate_token = os.getenv("REPLICATE_API_TOKEN")
if replicate_token:
    os.environ["REPLICATE_API_TOKEN"] = replicate_token

print("🔍 Searching for text-to-video models...")
print("=" * 50)

try:
    # Get all models and filter for video-related ones
    print("📋 Fetching available models...")
    
    video_models = []
    count = 0
    
    for model in replicate.models.list():
        count += 1
        if count > 100:  # Limit search to avoid too much output
            break
            
        # Check if model is related to video generation
        description = model.description or ""
        name = f"{model.owner}/{model.name}"
        
        video_keywords = ["video", "text-to-video", "t2v", "animate", "motion", "clip"]
        
        if any(keyword in description.lower() for keyword in video_keywords) or \
           any(keyword in name.lower() for keyword in video_keywords):
            video_models.append({
                "name": name,
                "description": description[:100] + "..." if len(description) > 100 else description
            })
    
    print(f"\n✅ Found {len(video_models)} video-related models:")
    print("=" * 50)
    
    for i, model in enumerate(video_models[:10], 1):  # Show first 10
        print(f"{i}. {model['name']}")
        print(f"   {model['description']}")
        print()
    
    if video_models:
        # Test the first few models
        print("🧪 Testing top models...")
        for model in video_models[:3]:
            try:
                print(f"\n📋 Testing: {model['name']}")
                
                # Try a simple test
                output = replicate.run(
                    model['name'],
                    input={"prompt": "a cat walking"},
                    wait=False
                )
                
                print(f"✅ {model['name']} - SUCCESS!")
                print(f"🎯 RECOMMENDED MODEL: {model['name']}")
                break
                
            except Exception as e:
                print(f"❌ {model['name']} - Failed: {str(e)[:100]}...")
                continue
    
except Exception as e:
    print(f"❌ Error searching models: {e}")
    
    # Fallback: try some known working models
    print("\n🔄 Trying fallback approach...")
    
    fallback_models = [
        "stability-ai/stable-video-diffusion",
        "fofr/stable-video-diffusion",
        "lucataco/stable-video-diffusion"
    ]
    
    for model in fallback_models:
        try:
            print(f"📋 Testing fallback: {model}")
            output = replicate.run(
                model,
                input={"image": "https://replicate.delivery/pbxt/JvEJQqJJqKgKiKwrjvYJH9H9cX9VgJF8xVGJQqJJqKgKiKwr.jpg"},
                wait=False
            )
            print(f"✅ {model} - SUCCESS!")
            print(f"🎯 RECOMMENDED MODEL: {model}")
            break
        except Exception as e:
            print(f"❌ {model} - Failed: {str(e)[:50]}...")

print("\n🎯 Search Complete!")