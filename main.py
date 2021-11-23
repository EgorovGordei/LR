import ContextFreeGrammar as ContextFreeGrammar_module
from ContextFreeGrammar import ContextFreeGrammar


ISTRING = "Input 'Y' if you want to see tables, anything else otherwise: "
ContextFreeGrammar_module.DEBUG = (input(ISTRING) == "Y")
rules = []
print("Input rules: (space to exit)")
while True:
    inp = input()
    if inp == " ":
        break
    rules.append(inp)

try:
    grammar = ContextFreeGrammar(rules)
except Exception as e:
    if e.args[0] == "Grammar is not LR(1)":
        print(e.args[0])
        exit()
    else:
        raise e


while True:
    text = input("\nText (space to exit): ")
    if text == " ":
        break

    try:
        parsing = grammar.checkLR1(text)
    except Exception:
        print("Word is not in grammar")
        continue

    if not parsing:
        print("Word is not in grammar")
    else:
        print("OK")
