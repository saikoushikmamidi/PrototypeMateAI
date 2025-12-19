from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_idea(idea, domain, complexity):
    prompt = f"""
You are a senior product architect at a prototyping company.

Analyze the following product idea and generate a complete prototype plan.

CLIENT IDEA:
{idea}

DOMAIN:
{domain}

COMPLEXITY:
{complexity}

Return ONLY valid JSON with EXACTLY these keys:

problem_statement: string (3–4 lines)
target_users: list of strings
mvp_features: list of strings
tech_stack: list of strings
timeline: string
success_metrics: list of strings
risks: list of strings
missing_requirements: list of strings
future_enhancements: list of strings
reference_links: list of valid URLs
executive_summary: string (6–8 lines, high-level summary)

RULES:
- No markdown
- No explanations
- No extra keys
- JSON ONLY
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25
    )

    raw = response.choices[0].message.content.strip()

    json_match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not json_match:
        raise ValueError(f"No JSON found:\n{raw}")

    return json.loads(json_match.group())
