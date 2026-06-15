"""
tools.py

The three required FitFindr tools. Each tool is a standalone function that
can be called and tested independently before being wired into the agent loop.

Complete and test each tool before moving to agent.py.

Tools:
    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)              → str
    create_fit_card(outfit, new_item)               → str
"""

import os

from dotenv import load_dotenv
from groq import Groq

from utils.data_loader import load_listings
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

import json
from config import DATA_PATH


with open(os.path.join(DATA_PATH, "./listings.json"), encoding="utf-8") as f:
    _listing = json.load(f)

with open(os.path.join(DATA_PATH, "./wardrobe_schema.json"), encoding="utf-8") as f:
    _wardobe = json.load(f)




# ── Groq client ───────────────────────────────────────────────────────────────

def _get_groq_client():
    """Initialize and return a Groq client using GROQ_API_KEY from .env."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root."
        )
    return Groq(api_key=api_key)

def call_llm(prompt: str, temperature: float = 0.4) -> str:
    client = _get_groq_client()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are FitFindr, a helpful fashion styling assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content
# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    print(_listing[0]) 
    """
    example of this print statemnet could be like:
    "title": "Faded Band Tee",
    "description": "vintage graphic tee",
    "size": "M",
    "price": 22,
    "platform": "Depop",
    "condition": "Good"
    """


    
    # If the user gave me a size and a price,
    # then enforce the size requirement. Otherwise, ignore size and price completely.

    results = []

    user_words = set(description.lower().split())

    for item in _listing:
        if size is not None and item["size"] != size:
            continue

        if max_price is not None and item["price"] > max_price:
            continue

        item_words = set(item["description"].lower().split())
        score = len(user_words & item_words)

        if score > 0:
            item["score"] = score
            results.append(item)


    results.sort(key=lambda x: x["score"], reverse=True)

    return results

# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    wardrobe_items = wardrobe.get("items", [])

    if not wardrobe_items:
        prompt = f"""
Give general styling ideas for this item:

{new_item}

The user has no wardrobe items saved, so suggest what kinds of pieces,
accessories, colors, and vibes would pair well with it.
"""
    else:
        prompt = f"""
Suggest specific outfit combinations using this new item:

{new_item}

Use these wardrobe items when possible:

{wardrobe_items}

Mention named pieces from the wardrobe and explain how they match.
"""

    return call_llm(prompt)

# ── Tool 3: create_fit_card ───────────────────────────────────────────────────
def create_fit_card(outfit: str, new_item: dict) -> str:
    if not outfit or not outfit.strip():
        return "I couldn't create a fit card because the outfit suggestion is missing."

    prompt = f"""
    Create a short, shareable outfit caption for this thrifted find.

    New item:
    Name: {new_item.get("title")}
    Price: ${new_item.get("price")}
    Platform: {new_item.get("platform")}

    Outfit suggestion:
    {outfit}

    Write 2-4 casual, authentic sentences like an Instagram or TikTok OOTD caption.
    Mention the item name, price, and platform naturally once each.
    Capture the outfit vibe in specific terms.
    Do not sound like a product description.
    """

    response = call_llm(prompt, temperature=0.8)
    return response