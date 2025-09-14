#!/usr/bin/env python3
"""
Find a working text-to-video model on Replicate
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import replicate

replicate_token = os.getenv("REPLICATE_API_TOKEN")
if replicate_token:
    os.environ["REPLICATE_API_TOKEN"] = replicate_token

print("🔍 Finding working text-to-video models...")
print("=" * 50)

# Try different models that are known to work
test_models = [
    "anotherjesse/zeroscope-v2-xl",
    "ali-vilab/i2vgen-xl", 
    "deforum/deforum_stable_diffusion",
    "lucataco/animate-diff"
]

working_models = []

for model_name in test_models:
    try:
        print(f"\n📋 Testing model: {model_name}")
        
        # Try to run the model with a simple prompt
        print("   Attempting to create prediction...")
        
        # Use replicate.run() which is simpler
        output = replicate.run(
            model_name,
            input={"prompt": "a cat walking"},
            wait=False  # Don't wait for completion, just test if it starts
        )
        
        print(f"✅ Model {model_name} works!")
        working_models.append(model_name)
        
    except Exception as e:
        print(f"❌ Model {model_name} failed: {str(e)}")

print("\n" + "=" * 50)
print("📊 RESULTS:")
print("=" * 50)

if working_models:
    print(f"✅ Found {len(working_models)} working models:")
    for model in working_models:
        print(f"   - {model}")
    
    print(f"\n🎯 RECOMMENDED: Use this model:")
    print(f"   {working_models[0]}")
else:
    print("❌ No working models found")
    print("💡 Let's try browsing available models...")
    
    # Try to list some models
    try:
        print("\n🔍 Browsing available models...")
        models = list(replicate.models.list())[:10]  # Get first 10
        for model in models:
            if "video" in model.description.lower() or "text" in model.description.lower():
                print(f"   📹 {model.owner}/{model.name}: {model.description[:60]}...")
    except Exception as e:
        print(f"❌ Error browsing models: {e}")

print("\n🎯 Test Complete!")