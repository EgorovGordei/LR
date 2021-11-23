from ContextFreeGrammar import ContextFreeGrammar


rules = []
N = int(input("Amount of rules: "))
print("Rules:")
for i in range(N):
    rules.append(input())
grammar = ContextFreeGrammar(rules)

while True:
    text = input("\nText (space to exit): ")
    if text == " ":
        break

    parsing = grammar.checkLR1(text)

    if parsing == False:
        print("Word is not in grammar")
    else:
        print("OK")
        #for i in range(len(parsing) - 1):
        #    print(parsing[i][0])
        #    print(" " * 16 + f"{parsing[i][1]} -> {parsing[i][2]}")
        #print(parsing[-1][0])
