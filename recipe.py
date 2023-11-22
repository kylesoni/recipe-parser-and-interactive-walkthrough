from ingredient import Ingredient
from step import Step

class Recipe:

    def __init__(self, scraped_ingredients, scraped_steps):
        
        self.ingredients = []
        self.steps = []
        self.tools = []
        self.methods = []

        self.current_step = 0

        for i in range(len(scraped_ingredients)):
            self.ingredients.append(Ingredient(scraped_ingredients[i]))

        for i in range(len(scraped_steps)):
            self.steps.append(scraped_steps[i])

    def test_ingredients(self):
        for i in range(len(self.ingredients)):
            print("Amount: " + self.ingredients[i].amount)
            print("Unit: " + self.ingredients[i].unit)
            print("Ing: " + self.ingredients[i].ingredient)
            print("Prep: " + self.ingredients[i].prep)
            print("Description: " + self.ingredients[i].desc)
            print("\n")