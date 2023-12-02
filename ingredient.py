import re
import copy
import spacy

# Get syntactic parser
spacy_model = spacy.load("en_core_web_sm")

class Ingredient:

    def __init__(self, ingredient_info):
        
        if not isinstance(ingredient_info, str):
            raise(Exception("Expected ingredient information to be a string."))

        ingredient_words = ingredient_info.split()

        self.amount = str(0)
        self.get_amount(ingredient_info)
        self.unit = ""
        self.get_unit(ingredient_info)
        self.ingredient = ""
        self.get_ingredient(ingredient_info)
        self.prep = ""
        self.desc = ""
        self.get_prep_and_descriptor()

    def get_amount(self, ingredient_info):
        ingredient_words = ingredient_info.split()
        amount_candidate = [ingredient_words[0], ingredient_words[1]]
        if not re.search('^[a-zA-Z,.?]+$', amount_candidate[0]):
            self.amount = amount_candidate[0]
            if not re.search('^[a-zA-Z,.?]+$', amount_candidate[1]):
                self.amount += amount_candidate[1]
        elif not re.search('^[a-zA-Z,.?]+$', amount_candidate[1]):
            self.amount = amount_candidate[1]

    def get_unit(self, ingredient_info):
        ingredient_words = ingredient_info.split()
        unit_candidates = ingredient_words[1:]
        actual_units = []
        for can in unit_candidates:
            if can in common_units:
                actual_units.append(common_units[can])
        if len(actual_units) >= 1:
            self.unit = actual_units[0]
        else:
            self.unit = ""
    
    def get_ingredient(self, ingredient_info):
        ingredient_words = ingredient_info.split()
        first = True
        for word in ingredient_words:
            if word not in self.amount and word not in common_units:
                if "(" not in word and ")" not in word:
                    if first:
                        self.ingredient = word
                        first = False
                    else:
                        self.ingredient += " " + word

    def get_prep_and_descriptor(self):
        prep_words = ""
        prep_candidates = []
        desc_words = []
        ingredient_words = self.ingredient.split()
        actual_ingredient_words = copy.deepcopy(ingredient_words)
        doc = spacy_model(self.ingredient)

        for word in ingredient_words:
            word = re.sub(r'[^\w\s]', '', word)
            if word in common_prep:
                for token in doc:
                    if token.text == word:
                        tracker = [token]
                        while len(tracker) > 0:
                            t = tracker.pop()
                            for child in t.children:
                                tracker.append(child)
                                if child.dep_ != "dobj" and child.pos_ != "VERB" and child.dep_ != "nsubj" and child.head.dep_ != "dobj":
                                    if child.text not in prep_candidates:
                                        prep_candidates.append(child.text)
                            if t.text not in prep_candidates:
                                prep_candidates.append(common_prep[token.text])
            elif word in common_descriptor:
                for token in doc:
                    if token.text == word:
                        for child in token.children:
                            if child.pos_ != "NOUN" and child.pos_ != "VERB":
                                desc_words.append(child.text)
                                actual_ingredient_words.remove(child.text)
                actual_ingredient_words.remove(word)

        for word in ingredient_words:
            raw_word = re.sub(r'[,.!?@#$%^&*_~]', '', word)
            if raw_word in prep_candidates:
                if prep_words == "":
                    prep_words = raw_word
                else:
                    prep_words += " " + raw_word
                actual_ingredient_words.remove(word)
        self.prep = prep_words

        if len(desc_words) > 0:
            self.desc = desc_words[0]
        for i in range(1, len(desc_words)):
            self.desc += ", " + desc_words[i]

        for i in range(len(actual_ingredient_words)):
            actual_ingredient_words[i] = re.sub(r'[,.!?@#$%^&*_~]', '', actual_ingredient_words[i])
        self.ingredient = ' '.join(actual_ingredient_words)
        
common_units = {
    'kg': 'kg',
    'lb.': 'lb',
    'pound': 'pound',
    'pounds': 'pounds',
    'g': 'g',
    'gram': 'g',
    'grams': 'g',
    'oz.': 'oz',
    'oz': 'oz',
    'ounce': 'oz',
    'ounces': 'oz',

    'inches': 'in',
    'in': 'in',
    
    'tsp': 'tsp',
    'tsp.': 'tsp',
    'teaspoon': 'tsp',
    'tbsp': 'Tbsp',
    'Tbsp': 'Tbsp',
    'Tbsp.': 'Tbsp',
    'tablespoons': 'Tbsp',
    
    'quarts': 'quarts',
    'quart' : 'quart',
    'cup' : 'cup',
    'cups' : 'cups',

    'sheet': 'sheet',
    'package': 'package',
    'clove': 'clove',
    'cloves': 'cloves',
    }

common_prep = {
    'diced': 'diced',
    'cubed': 'cubed',
    'beaten': 'beaten',
    'peeled': 'peeled',
    'softened': 'softened',
    'chopped': 'chopped',
    'cut' : 'cut'
}

common_descriptor = {
    'packed': 'packed',
    'all-purpose': 'all-purpose',
    'extra-virgin': 'extra-virgin',
    'large': 'large'
}


test_ingredient = Ingredient("4 cups peeled, cubed sweet potatoes")

# print(test_ingredient.ingredient)
# print(test_ingredient.amount)
# print(test_ingredient.unit)
# print(test_ingredient.prep)
# print(test_ingredient.desc)

# doc = spacy_model("4 cups peeled, cubed sweet potatoes")

# for token in doc:
#     # print(token.text, token.dep_, token.head.text, token.head.pos_,
#     #         [child for child in token.children])
#     # if token.text == "squares":
#     #     print(token.dep_)
#     print(token.text)