import re

from tools import search_listings, suggest_outfit, create_fit_card


def _new_session(query: str, wardrobe: dict) -> dict:
    return {
        "query": query,
        "wardrobe": wardrobe,
        "parsed": None,
        "search_results": None,
        "selected_item": None,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }


def _parse_query(query: str) -> dict:
    parsed = {
        "description": query,
        "size": None,
        "max_price": None,
    }

    price_match = re.search(r"(?:under\s*)?\$?(\d+(?:\.\d+)?)", query.lower())
    if price_match:
        parsed["max_price"] = float(price_match.group(1))

    size_match = re.search(r"(?:size|sz)\s+([a-zA-Z0-9]+)", query)
    if size_match:
        parsed["size"] = size_match.group(1).upper()

    description = query
    description = re.sub(r"under\s*\$?\d+(?:\.\d+)?", "", description, flags=re.I)
    description = re.sub(r"\$?\d+(?:\.\d+)?", "", description)
    description = re.sub(r"(?:in\s+)?(?:size|sz)\s+[a-zA-Z0-9]+", "", description, flags=re.I)
    description = " ".join(description.split())

    parsed["description"] = description

    return parsed


def run_agent(query: str, wardrobe: dict) -> dict:
    session = _new_session(query, wardrobe)

    parsed = _parse_query(query)
    session["parsed"] = parsed

    results = search_listings(
        description=parsed["description"],
        size=parsed["size"],
        max_price=parsed["max_price"],
    )

    session["search_results"] = results

    if not results:
        description = parsed["description"]
        size = parsed["size"]
        max_price = parsed["max_price"]

        message = f"I couldn't find anything for '{description}'"

        if size:
            message += f" in size {size}"

        if max_price:
            message += f" under ${max_price:.0f}"

        message += (
            ". Try using a broader search term, "
            "removing the size filter, or increasing your max price."
        )

        session["error"] = message
        return session

    selected_item = results[0]
    session["selected_item"] = selected_item

    outfit = suggest_outfit(selected_item, wardrobe)
    session["outfit_suggestion"] = outfit

    fit_card = create_fit_card(outfit, selected_item)
    session["fit_card"] = fit_card

    session["error"] = None
    return session