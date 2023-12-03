import spacy
import re

# Get syntactic parser
spacy_model = spacy.load("en_core_web_sm")

doc = spacy_model("1 (15 ounce) can kidney beans, drained")

for token in doc:
    # if token.text == "until":
    #     print([child for child in token.children])
    #     print(token.head)
    print([child for child in token.children])
    pass

#print(re.search("\(([^)]+)\)", "1 (16 ounce) bottle Italian dressing (such as Olive Garden℠ Signature Italian Dressing)").group(0))