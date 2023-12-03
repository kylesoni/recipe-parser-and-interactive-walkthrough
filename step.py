import re

class Step:

    def __init__(self, step_info, r_ingredients):
        
        self.text = step_info
        self.ingredients = []
        self.tools = []
        self.time = (0, "")

        self.get_ingredients(r_ingredients)

    def get_ingredients(self, ing_list):
        raw = self.text.lower()
        raw = re.sub(r'[^\w\s]', '', raw)
        for ing in ing_list:
            check_words = ing.ingredient.split()
            for word in check_words:
                if word in raw and ing.ingredient not in self.ingredients:
                    self.ingredients.append(ing.ingredient)