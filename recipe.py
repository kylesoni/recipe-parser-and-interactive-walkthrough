from ingredient import Ingredient
from step import Step

class Recipe:

    def __init__(self, scraped_ingredients, scraped_steps):
        
        self.ingredients = []
        self.steps = []
        self.tools = []
        self.methods = []

        self.current_step = -1

        for i in range(len(scraped_ingredients)):
            self.ingredients.append(Ingredient(scraped_ingredients[i]))

        for i in range(len(scraped_steps)):
            self.steps.append(Step(scraped_steps[i]))

    def progress_step(self):
        if self.current_step + 1 < len(self.steps):
            self.current_step += 1
            return self.steps[self.current_step]
        else:
            return "You have reached the end of the recipe!"

    def test_ingredients(self):
        for i in range(len(self.ingredients)):
            print("Amount: " + self.ingredients[i].amount)
            print("Unit: " + self.ingredients[i].unit)
            print("Ing: " + self.ingredients[i].ingredient)
            print("Prep: " + self.ingredients[i].prep)
            print("Description: " + self.ingredients[i].desc)
            print("\n")

    def test_steps(self):
        for i in range(len(self.steps)):
            print("Step: " + self.steps[i].text)
            print("\n")