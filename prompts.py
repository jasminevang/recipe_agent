# prompts.py
# Prompt for the GPT model when not using scraped recipes.
# Recipe includes attributes that interests me personally such as nutritional value.

def generate_recipe_prompt(dietary: str, meals: str, time_limit: str, protein: str) -> str:
    return f"""
I need help planning dinners for the week.

Please provide {meals} dinner recipes that follow these guidelines:
- Dietary preference: {dietary if dietary else 'no specific restrictions'}
- Maximum cooking time: {time_limit} minutes
- Preferred use of: {protein}
- Each recipe should include: 
    • A name
    • Serving Size
    • Cooking Time
    • Nutirtional value per serving showing Protein, Caleries, and Carbs
    • A short description
    • A list of ingredients

After listing the recipes, compile all ingredients into a single grocery list organized by category (like Produce, Pantry, Dairy, etc.).

Keep everything concise and easy to read.
"""