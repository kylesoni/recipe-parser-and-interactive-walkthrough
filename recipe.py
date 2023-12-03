from ingredient import Ingredient
from step import Step
import re

class Recipe:

    def __init__(self, scraped_ingredients, scraped_steps):
        
        self.ingredients = []
        self.steps = []
        self.tools = []
        self.methods = []
        self.ingredient_groups = {}

        self.current_step = -1

        current_category = "generic"
        for i in range(len(scraped_ingredients)):
            if ":" in scraped_ingredients[i]:
                current_category = re.sub(":", "", scraped_ingredients[i]).lower()
            else:
                ing = Ingredient(scraped_ingredients[i])
                self.ingredients.append(ing)
                if current_category in self.ingredient_groups:
                    self.ingredient_groups[current_category].append(ing.raw)
                else:
                    self.ingredient_groups[current_category] = [ing.raw]

        for i in range(len(scraped_steps)):
            self.steps.append(Step(scraped_steps[i], self.ingredients))

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
            print("")

    def test_ingredient_groups(self):
        keys = list(self.ingredient_groups.keys())
        for i in range(len(keys)):
            print(keys[i])
            print(self.ingredient_groups[keys[i]])
            print("")

    def test_steps(self):
        for i in range(len(self.steps)):
            print("Step: " + self.steps[i].text)
            print("Ingredients: " + str(self.steps[i].ingredients))
            print("")