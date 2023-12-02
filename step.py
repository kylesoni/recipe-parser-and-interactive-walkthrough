import re

class Step:

    def __init__(self, step_info):
        
        self.text = step_info
        self.ingredients = []
        self.tools = []
        self.time = (0, "")
        