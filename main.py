import ContextFreeGrammar as ContextFreeGrammar_module
from ContextFreeGrammar import ContextFreeGrammar


ContextFreeGrammar_module.DEBUG = (input("Input 'Y' if you want to see tables, anything else otherwise: ") == "Y")
rules = []
print("Input rules: (space to exit)")
while True:
    inp = input()
    if inp == " ":
        break
    rules.append(inp)
grammar = ContextFreeGrammar(rules)

while True:
    text = input("\nText (space to exit): ")
    if text == " ":
        break

    try:
        parsing = grammar.checkLR1(text)
    except:
        print("Word is not in grammar")
        continue

    if parsing == False:
        print("Word is not in grammar")
    else:
        print("OK")
 
