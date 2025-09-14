#!/usr/bin/env python3
"""
Test the prompt optimizer directly
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the optimizer
from app.services.prompt_optimizer import optimize_prompt

print("🧪 Testing Prompt Optimizer...")
print("=" * 50)

# Test the optimizer
test_prompt = "A robot fighting an ant"
test_style = "anime"

print(f"Input prompt: {test_prompt}")
print(f"Style: {test_style}")
print("\nOptimizing...")

result = optimize_prompt(test_prompt, test_style)

print(f"\nResult: {result}")
print("=" * 50)

# Check if it's still showing mock
if "[Optimized Mock]" in result:
    print("❌ Still showing mock response - API key issue")
else:
    print("✅ Real optimization working!")