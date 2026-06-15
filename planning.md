# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
It does get input of description, size and max_price, and then based on these values, takes a look
at listing.json to filter out and find the best matching options and retrun them

**Input parameters:**

<!-- List each parameter, its type, and what it represents -->

- `description` (str): like type of the cloth, is that a tee or pants, or etc?
- `size` (str): Size of the type of the cloth
- `max_price` (float): max price user can handle

**What it returns:**
Return value as Faded Band Tee — $22, Depop, Good condition."

**What happens if it fails or returns nothing:**
FitFindr tells the user what to try differently and stop so it doesnt call suggest_outfit

---

### Tool 2: suggest_outfit

**What it does:**
Gives advice on how to make it the complete the fit, how to macth certain accessories etc
**Input parameters:**
wardrobe and new_item

<!-- List each parameter, its type, and what it represents -->

- `new_item` (dict): whats given/chosen from seacrh_listing
- `wardrobe` (dict): what the user has already have

**What it returns:**
returns suggestion sentence and also makes a referral to user wardrobe to show how well it fits

**What happens if it fails or returns nothing:**
There is a get_empty_wardrobe() function, that would have been called

---

### Tool 3: create_fit_card

**What it does:**
Takes the suggestion, converts that and describes thats as a full complete look

**Input parameters:**

- `outfit` (str):takes outfit suggestion
- 'new_item' (str): what could be added

**What it returns:**

It returns full description of the look

**What happens if it fails or returns nothing:**
Should be using a helper function

---

### Additional Tools (if any)

---

## Planning Loop

**How does your agent decide which tool to call next?**

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

**How does information from one tool get passed to the next?**

## How does information from one tool get passed to the next?

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

## AI Tool Plan

I will use ChatGPT or Claude to help implement the FitFindr agent.
First, i will take a look at the functions by myself, and ry to complete them, then ask to AI what am I missing, how to make it better etc

I will verify the generated code by testing:

- A successful search that produces a complete Fit Card.
- A search with no matching listings.
- An empty wardrobe.
- Missing or incomplete outfit information.

I will compare the results to my planning document and architecture diagram to ensure the tools are called in the correct order and that failure cases are handled properly before moving on.

**Milestone 3 — Individual tool implementations:**

**Milestone 4 — Planning loop and state management:**

---

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
