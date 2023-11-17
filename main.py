from recipe_scrapers import scrape_me
from recipe import Recipe

url = "https://www.epicurious.com/recipes/food/views/tonkotsu-ramen"
scraper = scrape_me(url)

#print(scraper.ingredients())
#print(scraper.instructions_list())

test_recipe = Recipe(scraper.ingredients(), scraper.instructions_list())
print(test_recipe.steps)