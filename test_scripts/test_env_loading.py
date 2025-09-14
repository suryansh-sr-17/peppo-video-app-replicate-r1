#!/usr/bin/env python3
"""
Test script to verify environment variables are loaded correctly
"""
import os
from dotenv import load_dotenv

print("🔍 Testing environment variable loading...")
print("=" * 50)

# Load environment variables
load_dotenv()

# Test variables
test_vars = [
    "REPLICATE_API_TOKEN",
    "OPENAI_API_KEY", 
    "VIDEO_PROVIDER",
    "REPLICATE_MODEL"
]

print("📋 Environment Variables Status:")
for var in test_vars:
    value = os.getenv(var)
    if value:
        # Show first 10 and last 4 characters for security
        if len(value) > 20:
            masked_value = f"{value[:10]}...{value[-4:]}"
        else:
            masked_value = f"{value[:6]}..."
        print(f"✅ {var}: {masked_value}")
    else:
        print(f"❌ {var}: NOT FOUND")

print("\n" + "=" * 50)

# Test OpenAI connection
print("🧪 Testing OpenAI API connection...")
try:
    from openai import OpenAI
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        client = OpenAI(api_key=openai_key)
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )
        print(f"✅ OpenAI API: {response.choices[0].message.content}")
    else:
        print("❌ OpenAI API: No API key found")
except Exception as e:
    print(f"❌ OpenAI API Error: {str(e)}")

# Test Replicate connection
print("\n🧪 Testing Replicate API connection...")
try:
    import replicate
    
    replicate_token = os.getenv("REPLICATE_API_TOKEN")
    if replicate_token:
        os.environ["REPLICATE_API_TOKEN"] = replicate_token
        # Test by getting account info
        models = list(replicate.models.list())
        print(f"✅ Replicate API: Connected (found {len(models)} models)")
    else:
        print("❌ Replicate API: No API key found")
except Exception as e:
    print(f"❌ Replicate API Error: {str(e)}")

print("\n" + "=" * 50)
print("🎯 Test Complete!")