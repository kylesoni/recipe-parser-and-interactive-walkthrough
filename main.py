from recipe_scrapers import scrape_me

url = "https://www.epicurious.com/recipes/food/views/tonkotsu-ramen"
scraper = scrape_me(url)

print(scraper.ingredients())
print(scraper.instructions_list())