import os
import requests
import re
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Get the API key
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Cleaning function to remove unwanted characters like *, _, ~, etc.
def clean_text(text):
    # Remove common markdown or formatting characters
    text = re.sub(r'[*_~`#@^$=+{}\[\]|<>\\]', '', text)
    text = re.sub(r'\s{2,}', ' ', text)  # Collapse multiple spaces
    return text.strip()

# Function to format recipe into clean step-by-step HTML
def format_recipe_steps(raw_text):
    steps = re.split(r'(?:\n\d+[.)]\s|\n-\s|-\s|\n)', raw_text)
    steps = [step.strip() for step in steps if step.strip()]

    formatted = ""
    for i, step in enumerate(steps, 1):
        formatted += f"<p><b>Step {i}:</b> {step}</p>\n"
    return formatted

# Function to fetch recipe from OpenRouter API
def get_recipe(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Referer": "https://openrouter.ai",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3.3-8b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are an assistant who clarifies users queries."},
            {"role": "user", "content": f"Give me everything for {query} in detailed steps."}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    try:
        data = response.json()
        recipe_text = data["choices"][0]["message"]["content"]
        cleaned_text = clean_text(recipe_text)
        return format_recipe_steps(cleaned_text)

    except Exception as e:
        print("⚠️ API response error:", e)
        return "<p>Could not fetch recipe. Try again later.</p>"
