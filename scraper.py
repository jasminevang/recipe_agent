# scraper.py
# The scraper which finds recipes with the specified parameters, pulls the ingredients
# from the recipe, and returns a list of recipes and their attributes.

import requests
from bs4 import BeautifulSoup
import time
import random

# Link to ensure only dinner recipes are returned. The generic link can return sauces, desserts, etc.
BASE_URL = "https://www.recipetineats.com/category/collections/dinner-tonight/"

# Search RecipeTin Eats in the Dinner category with a keyword,
# go to a random page, and return random recipe URLs from that page.
def search_recipes(keyword: str, max_results: int = 3):

    # Use the base search URL with keyword to find the last page number
    search_url = f"{BASE_URL}/?s={keyword}"
    last_page_number = get_max_page_number(search_url)

    seen = set()
    collected_links = []

    while len(collected_links) < max_results:
        # choose random page
        chosen_page = random.randint(1, last_page_number)
        # Now get a random page of results
        page_url = f"{BASE_URL}/page/{chosen_page}/?s={keyword}"

        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, "html.parser")

        all_links = []

        # collect recipe links and pick a random one to save.
        for article in soup.select("article.post"):
            link_tag = article.find("a", href=True)
            if not link_tag:
                continue
            url = link_tag["href"]
            if url not in seen:
                all_links.append(url)
        if all_links:
            chosen_link = random.choice(all_links)
            collected_links.append(chosen_link)
            seen.add(chosen_link)

    return collected_links

# Given a URL, find the max/last page number
def get_max_page_number(base_url):
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, "html.parser")

    page_links = soup.select("a[href*='/page/']")

    page_numbers = []
    for link in page_links:
        href = link.get("href")
        if href:
            try:
                page_part = href.split("/page/")[1].split("/")[0]
                page_numbers.append(int(page_part))
            except (IndexError, ValueError):
                continue

    return max(page_numbers, default=1)

# Pull the recipe information from the recipes list
# Title, servings, time, description, ingredients, instructions
def scrape_recipe_page(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find("h2", class_="wprm-recipe-name wprm-block-text-bold")
    title = title.text.strip() if title else "Untitled Recipe"

    servings_tag = soup.find("div", class_="wprm-recipe-container")
    servings = servings_tag["data-servings"] if servings_tag and servings_tag.has_attr("data-servings") else "Unknown"

    total_time_tag = soup.find("span", class_="wprm-recipe-total_time")
    total_time = total_time_tag.text.strip() if total_time_tag else "Unknown"

    description_tag = soup.select_one("div.wprm-recipe-summary") 
    description = description_tag.text.strip() if description_tag else "No description found."

    ingredient_elements = soup.find_all("li", class_="wprm-recipe-ingredient")
    ingredients = []
    for li in ingredient_elements:
        amount = li.find("span", class_="wprm-recipe-ingredient-amount")
        unit = li.find("span", class_="wprm-recipe-ingredient-unit")
        name = li.find("span", class_="wprm-recipe-ingredient-name")
        text_parts = [
            amount.get_text(strip=True) if amount else "",
            unit.get_text(strip=True) if unit else "",
            name.get_text(strip=True) if name else ""
        ]
        ingredient_text = " ".join(part for part in text_parts if part)
        ingredients.append(ingredient_text)

    instructions = [i.text.strip() for i in soup.select("div.wprm-recipe-instruction-text")]

    return {
        "title": title,
        "servings": servings,
        "total_time": total_time,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "url": url
    }


def get_recipes_from_site(keyword="dinner", count=3):

    urls = search_recipes(keyword, max_results=count)
    recipes = []

    for url in urls:
        try:
            print(f"Recipe Link: {url}")
            recipe = scrape_recipe_page(url)
            recipes.append(recipe)
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
    
    return recipes

#test
from scraper import get_recipes_from_site

if __name__ == "__main__":
    recipes = get_recipes_from_site("chicken", 2)

    for r in recipes:
        print(r["title"])
        print("Ingredients:", r["ingredients"][:3], "...")