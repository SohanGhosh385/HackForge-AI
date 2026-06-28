import os
import time
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)

# Define system instruction and user prompt
system_instruction = (
    "You are HackForge AI, a world-class hackathon mentor.\n\n"
    "Generate EXACTLY 3 highly distinct hackathon project ideas based on inputs.\n"
    "Return JSON only matching the schema: {\"ideas\": [{\"title\": \"\", \"description\": \"\", \"tech_stack\": [\"\", \"\", \"\", \"\"], \"roadmap\": [\"\", \"\", \"\"], \"complexity_score\": 5, \"impact_score\": 5}], \"best_idea_index\": 0, \"ranking_reason\": \"\"}\n"
    "Keep descriptions under 30 words, tech_stack to exactly 4 items, and roadmaps to exactly 3 items."
)
user_prompt = "Generate ideas for Fintech & Banking domain, Intermediate level, 24 hours available."

# Test 1: Without response_schema
print("Test 1: Calling Gemini WITHOUT response_schema...")
start_time = time.time()
response1 = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=user_prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        temperature=0.3,
    ),
)
duration1 = time.time() - start_time
print(f"Test 1 Duration: {duration1:.2f} seconds")
print(f"Response 1 preview: {response1.text[:200]}...")

# Try to parse
try:
    parsed1 = json.loads(response1.text)
    print("Test 1 parsed successfully.")
except Exception as e:
    print(f"Test 1 parse failed: {e}")
