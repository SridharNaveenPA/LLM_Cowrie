import json
import requests
import sys
sys.path.insert(0, r'C:\Users\SridharNaveenPA\Downloads\HoneyPot - Kiro\honeypot_evaluator')
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

d = json.load(open(r'C:\Users\SridharNaveenPA\Downloads\HoneyPot - Kiro\honeypot_evaluator\attack_scenarios\credential_discovery.json'))
base_commands = [c['command'] for p in d['phases'] for c in p['commands']]
description = d.get('description', '')

system_prompt = (
    "You are a cybersecurity red team expert simulating realistic attacker behavior "
    "against a Linux SSH honeypot (Cowrie). Your role is to generate shell commands an attacker "
    "would realistically run.\n\n"
    "Only output a valid JSON array of shell command strings.\n"
    "No explanations, no markdown, just the JSON array."
)

user_prompt = (
    "Scenario: credential_discovery\n"
    "Description: " + description + "\n\n"
    "Base commands already planned:\n"
    + json.dumps(base_commands, indent=2) +
    "\n\nAdd up to 10 additional realistic commands. "
    "Keep ALL original commands and append new ones. "
    "Return a single flat JSON array of strings only. "
    'Example: ["command1", "command2"]'
)

payload = {
    "model": OLLAMA_MODEL,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt},
    ],
    "stream": False,
    "options": {"temperature": 0.4, "num_ctx": 8192},
}

print("Sending request to Ollama...")
r = requests.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=300)
print(f"Status: {r.status_code}")
raw = r.json()["message"]["content"]

print(f"\nTotal response length: {len(raw)} chars")
print("\n--- LAST 300 chars of output ---")
print(raw[-300:])
print("\n--- FULL OUTPUT ---")
print(raw)

# Try parsing
cleaned = raw.strip()
if "```" in cleaned:
    for part in cleaned.split("```"):
        part = part.strip()
        if part.startswith("json"):
            part = part[4:].strip()
        try:
            result = json.loads(part)
            print(f"\n✓ Parsed successfully after stripping markdown: {len(result)} commands")
            sys.exit(0)
        except Exception:
            continue

try:
    result = json.loads(cleaned)
    print(f"\n✓ Parsed directly: {len(result)} commands")
except json.JSONDecodeError as e:
    print(f"\n✗ JSON parse failed: {e}")
    # Find where the JSON starts and ends
    start = cleaned.find("[")
    end = cleaned.rfind("]")
    if start != -1 and end != -1:
        bracket_content = cleaned[start:end+1]
        print(f"  Trying bracket extraction [{start}:{end}]...")
        try:
            result = json.loads(bracket_content)
            print(f"  ✓ Bracket extraction worked: {len(result)} commands")
        except json.JSONDecodeError as e2:
            print(f"  ✗ Still failed: {e2}")
            print(f"  Content around error: {bracket_content[max(0,e2.pos-50):e2.pos+50]!r}")
