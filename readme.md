# Recipe Planner + Grocery List Generator

This project uses OpenAI's GPT-4o-mini and optionally real recipe data scraped from [recipetineats.com](https://www.recipetineats.com/) to help users plan a specified number of dinners and generate a categorized grocery list.

It supports both:
- Recipe scraping via BeautifulSoup from recipeTin eats
- AI-generated recipes via prompt-only fallback, or as choice

---

# Create Virtual Environment (Optional but Recommended)
'
python -m venv env # create python virt env
source env/bin/activate # activate python virt env (You'll have to do this every time)
'
# Install Dependencies
'
pip install openai
pip install python-dotenv
pip install requests
pip install beautifulsoup4 requests
'
# API Key

Create a .env file in the project root and paste your OpenAI key
'
OPENAI_API_KEY=your-openai-key-here
'

# Usage
'
python agent.py
'
The agent will prompt you for:
- Number of meals
- Ingredient or protein preference (e.g., chicken, spinach)
- Max cooking time
- Whether to use real recipes from RecipeTin Eats or GPT-generated ones

It will then generate:
A formatted summary of each recipe including:
- Name
- Servings
- Total time
- One-sentence description
- One-sentence prep tip
- Ingredient list
- A categorized grocery list (Produce, Protein, Pantry, etc.)

# Layout
'
recipe_agent/
├── agent.py              # Main program logic & LLM prompt formatting
├── scraper.py            # Web scraper for RecipeTin Eats (performs keyword search & random page pulls)
├── prompts.py            # Contains fallback prompt for GPT-only mode
├── .env                  # Stores OpenAI API key
├── .gitignore
├── venv/                 # Optional virtual environment
'