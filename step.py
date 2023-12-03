import re

class Step:

    def __init__(self, step_info, r_ingredients):
        
        self.text = step_info
        self.ingredients = []
        self.tools = []
        self.methods = []
        self.time = (0, "")

        self.get_ingredients(r_ingredients)
        self.get_tools()
        self.get_methods()

    def get_ingredients(self, ing_list):
        raw = self.text.lower()
        raw = re.sub(r'[^\w\s]', '', raw)
        raw = raw.split()
        for ing in ing_list:
            check_words = ing.ingredient.split()
            for word in check_words:
                check = word.split()
                flag = True
                for w in check:
                    if w not in raw:
                        flag = False
                if flag and ing.ingredient not in self.ingredients:
                        self.ingredients.append(ing.ingredient)
    
    def get_tools(self):
        raw = self.text.lower()
        raw = re.sub(r'[^\w\s]', '', raw)
        raw = raw.split()
        for word in list(common_tools.keys()):
            check = word.split()
            flag = True
            for w in check:
                if w not in raw:
                    flag = False
            if flag:
                tool = common_tools[word]
                if tool not in self.tools:
                    self.tools.append(tool)
    
    def get_methods(self):
        raw = self.text.lower()
        raw = re.sub(r'[^\w\s]', '', raw)
        raw = raw.split()
        for word in list(common_methods.keys()):
            check = word.split()
            flag = True
            for w in check:
                if w not in raw:
                    flag = False
            if flag:
                if word not in self.methods:
                    self.methods.append(word)
        for word in tools_for_methods:
            if word in raw:
                for tool in tools_for_methods[word]:
                    if tool not in self.tools:
                        self.tools.append(tool)

# partly from Wikipedia:  
common_tools = {
    "baster" : "baster",
    "beanpot" : "beanpot",
    "blowtorch" : "blowtorch",
    "bottle opener" : "bottle opener",
    "bowl" : "bowl",
    "bread knife" : "bread knife",
    "browning tray" : "browning tray",
    "butter curler" : "butter curler",
    "cake and pie server" : "cake and pie server",
    "candy thermometer" : "candy thermometer",
    "can opener" : "can opener",
    "cheese cutter" : "cheese cutter",
    "cheese knife" : "cheese knife",
    "cheese slicer" : "cheese slicer",
    "cheesecloth" : "cheesecloth",
    "chef's knife" : "chef's knife",
    "cherry pitter" : "cherry pitter",
    "chinois" : "chinois",
    "citrus reamer" : "citrus reamer",
    "clay pot" : "clay pot",
    "cleaver" : "cleaver",
    "colander" : "colander",
    "cookie cutter" : "cookie cutter",
    "cookie press" : "cookie press",
    "corkscrew" : "corkscrew",
    "crab cracker" : "crab cracker",
    "cutting board" : "cutting board",
    "edible tableware" : "edible tableware",
    "egg piercer" : "egg piercer",
    "egg poacher" : "egg poacher",
    "egg separator" : "egg separator",
    "egg slicer" : "egg slicer",
    "egg timer" : "egg timer",
    "flour sifter" : "flour sifter",
    "food mill" : "food mill",
    "funnel" : "funnel",
    "garlic press" : "garlic press",
    "grater" : "grater",
    "honey dipper" : "honey dipper",
    "honing steel" : "honing steel",
    "ladle" : "ladle",
    "lame" : "lame",
    "lemon squeezer" : "lemon squeezer",
    "lobster pick" : "lobster pick",
    "mandoline" : "mandoline",
    "measuring cup" : "measuring cup",
    "measuring spoon" : "measuring spoon",
    "meat grinder" : "meat grinder",
    "meat tenderizer" : "meat tenderizer",
    "meat thermometer" : "meat thermometer",
    "melon baller" : "melon baller",
    "mezzaluna" : "mezzaluna",
    "herb chopper" : "herb chopper",
    "microplane" : "microplane",
    "milk frother" : "milk frother",
    "milk watcher" : "milk watcher",
    "mortar and pestle" : "mortar and pestle",
    "nutcracker" : "nutcracker",
    "nutmeg grater" : "nutmeg grater",
    "oven glove" : "oven glove",
    "pastry bag" : "pastry bag",
    "pastry blender" : "pastry blender",
    "pastry brush" : "pastry brush",
    "pastry wheel" : "pastry wheel",
    "peeler" : "peeler",
    "pepper mill" : "pepper mill",
    "pie bird" : "pie bird",
    "pizza cutter" : "pizza cutter",
    "potato masher" : "potato masher",
    "potato ricer" : "potato ricer",
    "pot-holder" : "pot-holder",
    "pot" : "pot",
    "poultry shears" : "poultry shears",
    "roller docker" : "roller docker",
    "rolling pin" : "rolling pin",
    "salt and pepper shakers" : "salt and pepper shakers",
    "scissors" : "scissors",
    "scoop" : "scoop",
    "sieve" : "sieve",
    "slotted spoon" : "slotted spoon",
    "spatula" : "spatula",
    "spider" : "spider",
    "tamis" : "tamis",
    "tomato knife" : "tomato knife",
    "tongs" : "tongs",
    "trussing needle" : "trussing needle",
    "twine" : "twine",
    "weighing scale" : "weighing scale",
    "whisk" : "whisk",
    "wooden spoon" : "wooden spoon",
    "scraper" : "scraper",
    "saucepan" : "saucepan",
    "baking dish" : "baking dish",

    "air fryer" : "air fryer",
    "bachelor griller" : "bachelor griller",
    "barbecue grill" : "barbecue grill",
    "beehive oven" : "beehive oven",
    "brasero" : "brasero",
    "brazier" : "brazier",
    "bread machine" : "bread machine",
    "burjiko" : "burjiko",
    "butane torch" : "butane torch",
    "cheesemelter" : "cheesemelter",
    "chocolatera" : "chocolatera",
    "chorkor oven" : "chorkor oven",
    "clome oven" : "clome oven",
    "comal" : "comal",
    "combi steamer" : "combi steamer",
    "communal oven" : "communal oven",
    "convection microwave" : "convection microwave",
    "convection oven" : "convection oven",
    "corn roaster" : "corn roaster",
    "crepe maker" : "crepe maker",
    "deep fryer" : "deep fryer",
    "earth oven" : "earth oven",
    "electric cooker" : "electric cooker",
    "espresso machine" : "espresso machine",
    "field kitchen" : "field kitchen",
    "fire pot" : "fire pot",
    "flattop grill" : "flattop grill",
    "food steamer" : "food steamer",
    "fufu machine" : "fufu machine",
    "griddle" : "griddle",
    "halogen oven" : "halogen oven",
    "haybox" : "haybox",
    "hibachi" : "hibachi",
    "horno" : "horno",
    "hot box" : "hot box",
    "hot plate" : "hot plate",
    "instant pot" : "instant pot",
    "kamado" : "kamado",
    "kitchener range" : "kitchener range",
    "kujiejun" : "kujiejun",
    "kyoto box" : "kyoto box",
    "makiyakinabe" : "makiyakinabe",
    "masonry oven" : "masonry oven",
    "mess kit" : "mess kit",
    "microwave" : "microwave",
    "microwave oven" : "microwave oven",
    "multicooker" : "multicooker",
    "oven" : "oven",
    "pancake machine" : "pancake machine",
    "panini sandwich grill" : "panini sandwich grill",
    "popcorn maker" : "popcorn maker",
    "pressure cooker" : "pressure cooker",
    "pressure fryer" : "pressure fryer",
    "reflector oven" : "reflector oven",
    "remoska" : "remoska",
    "rice cooker" : "rice cooker",
    "rice polisher" : "rice polisher",
    "roasting jack" : "roasting jack",
    "rocket mass heater" : "rocket mass heater",
    "rotimatic" : "rotimatic",
    "rotisserie" : "rotisserie",
    "russian oven" : "russian oven",
    "sabbath mode" : "sabbath mode",
    "salamander broiler" : "salamander broiler",
    "samovar" : "samovar",
    "sandwich toaster" : "sandwich toaster",
    "self-cleaning oven" : "self-cleaning oven",
    "shichirin" : "shichirin",
    "slow cooker" : "slow cooker",
    "solar cooker" : "solar cooker",
    "sous-vide" : "sous-vide",
    "soy milk maker" : "soy milk maker",
    "stove" : "stove",
    "susceptor" : "susceptor",
    "tabun oven" : "tabun oven",
    "tandoor" : "tandoor",
    "tangia" : "tangia",
    "thermal immersion circulator" : "thermal immersion circulator",
    "toaster" : "toaster",
    "turkey fryer" : "turkey fryer",
    "vacuum fryer" : "vacuum fryer",
    "waffle iron" : "waffle iron",
    "wet grinder" : "wet grinder",
    "wine cooler" : "wine cooler"
}

common_methods = {
    "bake" : "bake",
    "barbecue" : "barbecue",
    "blanch" : "blanch",
    "boil" : "boil",
    "braise" : "braise",
    "brine" : "brine",
    "broast" : "broast",
    "browne" : "browne",
    "carmelize" : "caramelize",
    "coddle" : "coddle",
    "curdle" : "curdle",
    "cure" : "cure",
    "deep fry" : "deep fry",
    "dry" : "dry",
    "emulsify" : "emulsify",
    "ferment" : "ferment",
    "fry" : "fry",
    "garnish" : "garnish",
    "glaze" : "glaze",
    "grill" : "grill",
    "juice" : "juice",
    "marinate" : "marinate",
    "mince" : "mince",
    "pan fry" : "pan fry",
    "pasteurize" : "pasteurize",
    "pickle" : "pickle",
    "roast" : "roast",
    "sauté" : "saute",
    "saute" : "saute",
    "seare" : "seare",
    "shuck" : "shuck",
    "smoke" : "smoke",
    "steam" : "steam",
    "stir fry " : " stir fry"
}

tools_for_methods = {
    "saute" : ["pan"],
    "sauté" : ["pan"],
    'combine': ['spoon', 'bowl'],
    'whip': ['whisk'],
    'simmer': ['pot'],
    'grill': ['grill'],
    'char': ['grill'],
    'carmelize': ['pan'],
    'stir to combine': ['spoon', 'bowl'],
    'stir': ['spoon', 'bowl'],
    'blanche': ['pot', 'strainer', 'ice bath'],
    'braise': ['saucepan', 'oven'],
    'fry': ['pot', 'strainer'],
    'hard-boil': ['pot'],
    'soft-boil': ['pot'],
    'stew': ['large saucepot'],
    'pulverize': ['mortar and pestle'],
    'grind': ['mortar and pestle'],
    'pan-fry': ['pan'],
    'melt': ['bowl'],
    'mash': ['potato masher/fork'],
    'poach': ['sauce pot'],
    'bake': ['oven'],
    'drain': [],
    'sear': ['pan'],
    'scramble': ['whisk'],
    'reduce': ['sauce pot']
}