# FitFindr — README.md

FitFindr is a fashion recommendation agent that helps users find secondhand clothing items and generate outfit ideas.
### Tool 1: search_listings

**What it does:**
It does get input of description, size and max_price, and then based on these values, takes a look
at listing.json to filter out and find the best matching options and retrun them

## Planning Loop

The agent follows this workflow:

1. Call `search_listings`.
   - Uses the user's description, size, and budget to find matching items.
   - If no listings are found, the agent tells the user to adjust their search criteria and stops.

2. Call `suggest_outfit`.
   - Uses the selected item and the user's wardrobe to generate styling recommendations.
   - If wardrobe data is missing, the helper function `get_empty_wardrobe()` is used.
   - If no suggestions can be generated, the agent returns a fallback styling message.

3. Call `create_fit_card`.
   - Combines the selected item and outfit suggestions into a complete outfit description.
   - Returns a final "Fit Card" showing the recommended look.

## The process ends after the Fit Card is generated and returned to the user.

## State Management

The agent stores information in a session state object throughout the conversation.

Tracked data includes:

- User clothing description
- Desired size
- Maximum budget
- Selected listing from search_listings
- User wardrobe data
- Outfit recommendations

Data flow:

1. `search_listings`
   - Receives description, size, and max_price.
   - Returns the best matching clothing item.
   - The returned item is stored as `selected_item`.

2. `suggest_outfit`
   - Receives `selected_item` and `wardrobe`.
   - Generates styling recommendations.
   - Stores the result as `outfit_suggestion`.

3. `create_fit_card`
   - Receives `selected_item` and `outfit_suggestion`.
   - Creates a complete Fit Card describing the final look.

The agent passes outputs from one tool directly into the inputs of the next tool until the final recommendation is generated.

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool            | Failure mode                          | Agent response                                                                   |
| --------------- | ------------------------------------- | -------------------------------------------------------------------------------- |
| search_listings | No results match the query            | Stop the workflow and ask the user to adjust their description, size, or budget. |
| suggest_outfit  | Wardrobe is empty                     | call get_wardrobeempty helpfer function                                          |
| create_fit_card | Outfit input is missing or incomplete | Use fallback data from get_empty_wardrobe() or return a simplified Fit Card.     |

---

## Architecture

     ## Architecture

User Query
│
▼
Planning Loop
│
│ reads user inputs:
│ description, size, max_price
│
▼
search_listings(description, size, max_price)
│
├── results = []
│ ▼
│ [ERROR] No listings found
│ ▼
│ Return message asking user to change search
│
└── results = [item, ...]
▼
Session State:
selected_item = results[0]
│
▼
suggest_outfit(selected_item, wardrobe)
│
├── wardrobe is empty
│ ▼
│ get_empty_wardrobe()
│ ▼
│ Generate basic styling advice
│
└── outfit suggestion created
▼
Session State:
outfit_suggestion = suggestion
│
▼
create_fit_card(outfit_suggestion, selected_item)
│
├── missing outfit data
│ ▼
│ [ERROR] Return simplified Fit Card
│
└── fit card created
▼
Session State:
fit_card = final look description
│
▼
Return Fit Card to User

## AI Tool Plan

I used ChatGPT and Claude to help implement the FitFindr agent.
First, i took a look at the functions by myself, and ry to complete them, then ask to AI what am I missing, how to make it better etc

I verified the generated code by testing:

- A successful search that produces a complete Fit Card.
- A search with no matching listings.
- An empty wardrobe.
- Missing or incomplete outfit information.

## A Complete Interaction (Step by Step)

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**

The agent calls search_listing with :
description="vintage graphic tee",
size="M",
max_price=30

The tool searches listings.json and returns:

{
"title": "Faded Band Tee",
"price": 22,
"platform": "Depop",
"condition": "Good"
}

**Step 2:**
The agent calls:

suggest_outfit(
selected_item,
wardrobe={
"pants": ["baggy jeans"],
"shoes": ["chunky sneakers"]
}
)

The tool returns:

"Pair the Faded Band Tee with your baggy jeans and chunky sneakers. Add a silver chain and oversized jacket for a vintage streetwear look."

The result is stored as: outfit_suggestion = "Pair the Faded Band Tee..."

**Step 3:**

The agent calls:

create_fit_card(
outfit_suggestion,
selected_item
)

The tool generates a complete Fit Card describing the outfit.

The result is stored as: fit_card = "Vintage streetwear outfit featuring..."

**Final output to user:**

Recommended Item: Faded Band Tee ($22, Depop, Good Condition)

Style Suggestion: Pair it with your baggy jeans and chunky sneakers.
Add a silver chain and oversized jacket.

Fit Card: A vintage-inspired streetwear outfit centered around the Faded Band Tee. The relaxed fit of the baggy jeans and chunky sneakers creates a balanced casual look, while the accessories add personality and complete the outfit.
