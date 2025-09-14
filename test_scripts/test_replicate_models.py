#!/usr/bin/env python3
"""
Test script to find working text-to-video models on Replicate
"""
import os
import replicate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up API token
replicate_token = os.getenv("REPLICATE_API_TOKEN")
if not replicate_token:
    print("❌ REPLICATE_API_TOKEN not found in .env file")
    exit(1)

os.environ["REPLICATE_API_TOKEN"] = replicate_token

# List of potential text-to-video models to test
test_models = [
    "ali-vilab/i2vgen-xl",
    "anotherjesse/zeroscope-v2-xl", 
    "deforum/deforum_stable_diffusion",
    "cjwbw/damo-text-to-video",
    "lucataco/animate-diff"
]

print("🔍 Testing Replicate text-to-video models...")
print("=" * 50)

working_models = []

for model_name in test_models:
    try:
        print(f"\n📋 Testing model: {model_name}")
        
        # Try to get model info
        model = replicate.models.get(model_name)
        print(f"✅ Model found: {model.name}")
        print(f"   Description: {model.description[:100]}...")
        
        # Get latest version
        if model.versions.list():
            latest_version = model.versions.list()[0]
            full_model_id = f"{model_name}:{latest_version.id}"
            print(f"   Latest version: {latest_version.id}")
            print(f"   Full model ID: {full_model_id}")
            
            working_models.append({
                "name": model_name,
                "full_id": full_model_id,
                "description": model.description
            })
        else:
            print("⚠️  No versions found")
            
    except Exception as e:
        print(f"❌ Error with {model_name}: {str(e)}")

print("\n" + "=" * 50)
print("📊 SUMMARY:")
print("=" * 50)

if working_models:
    print(f"✅ Found {len(working_models)} working models:")
    for i, model in enumerate(working_models, 1):
        print(f"\n{i}. {model['name']}")
        print(f"   Full ID: {model['full_id']}")
        print(f"   Description: {model['description'][:100]}...")
    
    print(f"\n🎯 RECOMMENDED: Use this in your .env file:")
    print(f"REPLICATE_MODEL={working_models[0]['full_id']}")
else:
    print("❌ No working text-to-video models found")
    print("💡 Try searching Replicate's website for current text-to-video models")

print("\n🔗 You can also browse models at: https://replicate.com/collections/text-to-video")