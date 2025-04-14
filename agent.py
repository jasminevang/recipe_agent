# agent.py
# Driver for the recipe planner, collecting user input regarding how the recipes
# are generated and the parameters.

import os
from dotenv import load_dotenv
from openai import OpenAI
from scraper import get_recipes_from_site
from prompts import generate_recipe_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    # Greeting and parameter collection
    print("Welcome to your Recipe Planner!\n")

    use_real = input("Do you want to use recipes from RecipeTin Eats? (yes/no): ").lower().strip() == "yes"
    preference = input("Any protein or ingredient preference? (e.g. beef, chicken, spinach, none): ")
    meals = input("How many dinners do you want to plan?: ")

    # Use recipes from RecipeTin Eats
    if use_real:
        print("\nSearching for recipes...\n")
        recipes = get_recipes_from_site(preference or "dinner", int(meals))

        if not recipes:
            print("No valid recipes found. We'll use GPT-generated recipes.\n")
            # Dietary and time limit not supported for online recipes and therefor not previously collected.
            dietary = ""
            time_limit = ""
            prompt = generate_recipe_prompt(dietary, meals, time_limit, preference)
        else:
            # Format scraped recipes for the LLM
            recipe_blocks = []
            combined_ingredients = []

            for r in recipes:
                recipe_block = f"""
                    {r['title']}
                    Servings: {r['servings']}
                    Total Time: {r['total_time']}
                    Description: {r['description']}
                    Ingredients:
                    {chr(10).join('- ' + i for i in r['ingredients'])}
                """
                recipe_blocks.append(recipe_block)
                combined_ingredients.extend(r['ingredients'])

            formatted_recipes = "\n\n".join(recipe_blocks)

            # Prompt to GPT regarding formatting and information to return to user.
            prompt = f"""
                You are helping someone plan their weekly dinners using real recipes. Format your response using the structure below for each recipe.

                For each recipe:
                Recipe Name  
                Servings: X  
                Total Time: Y  
                Description: (1 sentence summary of the meal)  
                Tip: (1 helpful sentence about preparing this recipe)  
                Ingredients:  
                - item 1  
                - item 2  
                ...

                After listing all recipes, combine all ingredients into a single categorized grocery list (e.g. Produce, Protein, Dairy, Spices, Pantry, etc).

                Here are the recipes and ingredients:

                {formatted_recipes}

                Combined Ingredient List:
                {chr(10).join(combined_ingredients)}
            """
    # Use generated GPT recipes, can have more recipe parameters.
    else:
        dietary = input("Any dietary restrictions? (e.g. vegetarian, gluten-free, none): ")
        time_limit = input("Max cooking time (in minutes)?: ")
        prompt = generate_recipe_prompt(dietary, meals, time_limit, preference)

    print("\nGive me a moment to format your recipes and grocery list...\n")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    #print_response(response)
    content = response.choices[0].message.content
    print(content)

if __name__ == "__main__":
    main()
