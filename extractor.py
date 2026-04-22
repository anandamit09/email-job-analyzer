from groq import Groq
import json
import re

client = Groq(api_key="your_api_key_here")


def clean_response(text):
    # Remove ```json ... ```
    if text.startswith("```"):
        text = re.sub(r"```[a-zA-Z]*", "", text)
        text = text.replace("```", "")
    return text.strip()


def fallback_role_detection(email_text):
    text = email_text.lower()

    keywords = [
        "software engineer", "developer", "frontend", "backend",
        "full stack", "sde", "analyst", "consultant",
        "engineer", "intern", "trainee", "tester", "qa"
    ]

    for word in keywords:
        if word in text:
            return word.title()

    return None


def extract_info(email_text):
    email_text = email_text[:4000]

    prompt = f"""
You are an expert system extracting job data from placement emails.

IMPORTANT:
- These are placement/job emails
- Extract role even if it's Analyst, Consultant, GET, Intern, etc.

Return ONLY valid JSON:

{{
  "company": "string",
  "role": "string or null",
  "package": "string or null",
  "location": "string or null"
}}

Rules:
- NO markdown
- NO ```
- Extract role exactly as written
- If multiple roles → combine
- If missing → null
- Return null ONLY if completely unrelated

Email:
{email_text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        text = response.choices[0].message.content.strip()

        print("RAW RESPONSE:", text)

        if text.lower() == "null":
            return None

        text = clean_response(text)

        try:
            data = json.loads(text)
        except Exception:
            print("JSON ERROR TEXT:", text)
            return None

        # 🔥 FALLBACK ROLE FIX
        if not data.get("role"):
            fallback_role = fallback_role_detection(email_text)
            if fallback_role:
                data["role"] = fallback_role

        return data

    except Exception as e:
        print("ERROR:", e)
        return None