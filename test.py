from ContextFreeGrammar import ContextFreeGrammar, Rule


def test_rule():
    rule = Rule("A->B")
    assert(str(rule) == "A->.B:")


def test_custom0_0():
    rules = ["S->abSb", "S->bbT", "T->aTT", "T->a"]
    text = "abbbab"
    grammar = ContextFreeGrammar(rules)
    assert(grammar.checkLR1(text))


def test_custom0_1():
    rules = ["S->abSb", "S->bbT", "T->aTT", "T->a"]
    text = "abbbaba"
    grammar = ContextFreeGrammar(rules)
    assert(not grammar.checkLR1(text))


def test_custom_1_0():
    rules = ["S->CC", "C->cC", "C->d"]
    text = "dd"
    grammar = ContextFreeGrammar(rules)
    assert(grammar.checkLR1(text))


def test_custom_1_1():
    rules = ["S->CC", "C->cC", "C->d"]
    text = "cc"
    grammar = ContextFreeGrammar(rules)
    assert(not grammar.checkLR1(text))


def test_custom_1_2():
    rules = ["S->CC", "C->cC", "C->d"]
    text = "dccccd"
    grammar = ContextFreeGrammar(rules)
    assert(grammar.checkLR1(text))


def test_custom_2_0():
    rules = ["S->S+T", "S->T", "T->T*F", "T->F", "F->(S)", "F->x"]
    text = "x+x*x"
    grammar = ContextFreeGrammar(rules)
    assert(grammar.checkLR1(text))


def test_custom_2_1():
    rules = ["S->S+T", "S->T", "T->T*F", "T->F", "F->(S)", "F->x"]
    text = "(x+x)*(x*x+x)"
    grammar = ContextFreeGrammar(rules)
    assert(grammar.checkLR1(text))


def test_custom_2_2():
    rules = ["S->S+T", "S->T", "T->T*F", "T->F", "F->(S)", "F->x"]
    text = "(x)+x*x"
    grammar = ContextFreeGrammar(rules)
    assert(grammar.checkLR1(text))


def test_custom_2_3():
    rules = ["S->S+T", "S->T", "T->T*F", "T->F", "F->(S)", "F->x"]
    text = "x+()+x*x"
    grammar = ContextFreeGrammar(rules)
    assert(not grammar.checkLR1(text))


def test_custom_3_0():
    rules = ["S->S+T", "S->T", "T->T*F", "T->F", "F->(S)", "F->"]
    text = "+()+*"
    grammar = ContextFreeGrammar(rules)
    assert(grammar.checkLR1(text))


def test_custom_3_1():
    rules = ["S->S+T", "S->T", "T->T*F", "T->F", "F->(S)", "F->"]
    text = "+()()+*"
    grammar = ContextFreeGrammar(rules)
    assert(not grammar.checkLR1(text))


def test_custom_4_0():
    rules = ["S->A is A", "A->BC", "B->a ", "B->the ", "B->", "C->math", "C->pleasure"]
    text = "a math is pleasure"
    grammar = ContextFreeGrammar(rules)
    assert(grammar.checkLR1(text))


def test_custom_4_1():
    rules = ["S->A is A", "A->BC", "B->a ", "B->the ", "B->", "C->math", "C->pleasure"]
    text = "the math is a pleasure"
    grammar = ContextFreeGrammar(rules)
    assert(grammar.checkLR1(text))


def test_custom_4_2():
    rules = ["S->A is A", "A->BC", "B->a ", "B->the ", "B->", "C->math", "C->pleasure"]
    text = " math is a pleasure"
    grammar = ContextFreeGrammar(rules)
    assert(not grammar.checkLR1(text))

