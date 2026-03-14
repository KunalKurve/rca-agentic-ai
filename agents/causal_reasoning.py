from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_json_from_text(text: str):
    """
    Extract JSON from:
    1. ```json ... ```
    2. raw {...}
    """
    if not text:
        return None

    fenced_match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced_match:
        return fenced_match.group(1)

    raw_match = re.search(r"(\{.*\})", text, re.DOTALL)
    if raw_match:
        return raw_match.group(1)

    return None

def generate_causal_path(state):
    prompt = f"""
You are an expert industrial root cause analysis engineer.

Analyze the following inputs and return ONLY valid JSON.
Do not include markdown fences.
Do not include explanation outside the JSON.

User Query:
{state.get('input', '')}

Sensor Logs:
{state.get('logs', [])}

Maintenance History:
{state.get('maintenance_history', [])}

Detected Anomalies:
{state.get('anomalies', [])}

Retrieved SOP / Incident Documents:
{state.get('retrieved_docs', [])}

Return JSON in this exact format:
{{
  "problem": "...",
  "evidence": ["...", "..."],
  "steps": ["...", "..."],
  "root_cause": "...",
  "confidence": "high/medium/low"
}}
"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert industrial RCA analyst. "
                        "Return only valid JSON. No markdown. No commentary."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500,
            temperature=0.1
        )

        output = response.choices[0].message.content.strip()
        json_text = extract_json_from_text(output)

        if json_text:
            try:
                causal_json = json.loads(json_text)
            except json.JSONDecodeError:
                causal_json = {
                    "problem": "Parsing failed",
                    "evidence": [],
                    "steps": [],
                    "root_cause": output,
                    "confidence": "low"
                }
        else:
            causal_json = {
                "problem": "Parsing failed",
                "evidence": [],
                "steps": [],
                "root_cause": output,
                "confidence": "low"
            }

        return {
            **state,
            "causal_analysis": causal_json
        }

    except Exception as e:
        return {
            **state,
            "causal_analysis": {
                "problem": "LLM call failed",
                "evidence": [],
                "steps": [],
                "root_cause": str(e),
                "confidence": "low"
            },
            "error": str(e)
        }