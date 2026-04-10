import requests
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_linkedin_url(prompt: str):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{
            "parts": [{
                "text": f"""
Convert this query into LinkedIn people search URL only.

Query: {prompt}

Return ONLY URL. No explanation.
"""
            }]
        }]
    }

    response = requests.post(url, json=payload)
    data = response.json()
    print(data)


    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip()
    except:
        return None