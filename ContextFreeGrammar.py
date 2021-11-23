# if set True will print tables
DEBUG = True


class Rule():
    '''Contains letter, word, dot and i of rule'''
    def __init__(self, rule, dot=0, i="", parents=[]):
        self.letter = rule[0:rule.index("->")]
        self.word = rule[rule.index("->") + 2:]
        self.dot = dot
        self.i = i

    def whole(self):
        return self.letter + "->" + self.word

    def __eq__(self, other):
        return self.letter == other.letter and self.word == other.word and \
               self.dot == other.dot and self.i == other.i

    def __repr__(self):
        return str(self.letter) + "->" + str(self.word[0:self.dot]) + \
               "." + str(self.word[self.dot:]) + ":" + str(self.i)


class ContextFreeGrammar():
    def __init__(self, rules):
        # create rules
        self.rules = [Rule(rule) for rule in rules]
        self.rules.append(Rule("$->S"))
        # prepare grammar for parsing
        self.setEpsylon()
        self.setFirst()
        self.terminals = set()
        for rule in self.rules:
            for a in rule.word:
                if a not in self.first.keys():
                    self.terminals.add(a)
        self.fillTable()

    def setEpsylon(self):
        # constructs self.epsylon such that:
        #   self.epsylon[nonterminal] = True <=> nonterminal -> ""
        self.epsylon = dict()
        nonterminals = set(rule.letter for rule in self.rules)
        for nt in nonterminals:
            self.epsylon[nt] = False
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if not self.epsylon[rule.letter] and self.isE(rule.word):
                    changed = True
                    self.epsylon[rule.letter] = True
        if DEBUG:
            print("Epsylon: ", self.epsylon)

    def isE(self, word):
        # {"#"} if word -> "" else {}
        for letter in word:
            if letter not in self.epsylon or not self.epsylon[letter]:
                return set()
        return {"#"}

    def getFirst(self, text):
        # first + check_empty
        if len(text) == 0:
            return ["#"]
        if text[0] in self.first.keys():
            return self.first[text[0]] | self.isE(text)
        return text[0]

    def closure(self, situations):
        # for every situation S->alpha.Bbeta add rules B->.gamma
        ans = []
        for sit in situations:
            ans.append(Rule(sit.whole(), sit.dot, sit.i))
        i = 0
        while i < len(ans):
            sit = ans[i]
            for rule in self.rules:
                if sit.dot >= len(sit.word):
                    continue
                if sit.word[sit.dot] == rule.letter:
                    for c in self.getFirst(sit.word[sit.dot + 1:] + sit.i):
                        new_rule = Rule(rule.whole(), 0, c)
                        if new_rule not in ans:
                            ans.append(new_rule)
            i += 1
        return tuple(ans)

    def goto(self, situations, nonterminal):
        # S->alpha.cbeta, nonterminal=c => add S->alphac.beta to answer
        if len(nonterminal) != 1:
            raise Exception("goto: len(nonterminal) != 1")
        if len(nonterminal) == 1:
            ans = []
            for sit in situations:
                if sit.dot >= len(sit.word):
                    continue
                if sit.word[sit.dot] == nonterminal:
                    ans.append(Rule(sit.whole(), sit.dot + 1, sit.i))
            ans = self.closure(ans)
            return ans

    def setFirst(self):
        dependencies = dict()
        # all non-terminals
        for rule in self.rules:
            dependencies[rule.letter] = set()
        # fill dependencies
        for rule in self.rules:
            if len(rule.word) > 0 and rule.word[0] in dependencies.keys():
                dependencies[rule.letter].add(rule.word[0])
        # fill first array (simple parts)
        terminals = dict()
        for rule in self.rules:
            terminals[rule.letter] = set()
        for rule in self.rules:
            if len(rule.word) > 0 and rule.word[0] not in dependencies.keys():
                terminals[rule.letter].add(rule.word[0])
        # fill first array
        self.first = dict()
        for nonterm in dependencies.keys():
            # add terms from all nonterms achievable from current
            used = set(nonterm)
            dfs = [nonterm]
            self.first[nonterm] = set()
            while len(dfs) > 0:
                cur = dfs[0]
                dfs = dfs[1:]
                for nex in dependencies[cur]:
                    if nex not in used:
                        used.add(nex)
                        dfs.append(nex)
                for term in terminals[cur]:
                    self.first[nonterm].add(term)
        if DEBUG:
            print("First: ", self.first)

    def fillTable(self):
        # initialise Q - all states
        # set array: goto_transitions[(i, a)] = j <=> self.goto(q[i], a) = j
        Q = [self.closure([Rule("$->S", 0, "#")])]
        goto_transitions = dict()
        i = 0
        while i < len(Q):
            for a in self.terminals | self.first.keys():
                new_state = self.goto(Q[i], a)
                if len(new_state) == 0:
                    goto_transitions[(i, a)] = -1
                elif new_state not in Q:
                    Q.append(new_state)
                    goto_transitions[(i, a)] = len(Q) - 1
                else:
                    goto_transitions[(i, a)] = Q.index(new_state)
            i += 1
        if DEBUG:
            print("Situations")
            for i in range(len(Q)):
                print(i, Q[i])
        # empty self.table_goto and self.table_action
        self.table_goto = dict()
        self.table_action = dict()
        for q_ind in range(len(Q)):
            for A in self.first.keys():
                self.table_goto[(q_ind, A)] = set()
            for a in self.terminals:
                self.table_action[(q_ind, a)] = set()
            self.table_action[(q_ind, "#")] = set()

        # fill table
        for q_ind in range(len(Q)):
            q = Q[q_ind]
            # ACTION
            for a in self.terminals | set("#"):
                exit = False
                # shift
                for rule_ind in range(len(q)):
                    rule = q[rule_ind]
                    if rule.dot < len(rule.word) and rule.word[rule.dot] == a:
                        exit = True
                        if goto_transitions[(q_ind, a)] != -1:
                            action = "s" + str(goto_transitions[(q_ind, a)])
                            self.table_action[(q_ind, a)].add(action)
                if exit:
                    continue
                # accept or reduce
                for rule_ind in range(len(q)):
                    rule = q[rule_ind]
                    if rule.dot == len(rule.word) and rule.i == a:
                        key = (q_ind, a)
                        rule_pos = self.rules.index(Rule(rule.whole()))
                        if rule_pos == len(self.rules) - 1:
                            self.table_action[key].add("a")
                        else:
                            self.table_action[key].add("r" + str(rule_pos))
                        exit = True
                if exit:
                    continue
                # accept
                for rule_ind in range(len(q)):
                    rule = q[rule_ind]
                    example = Rule("$->S")
                    example.dot = 1
                    example.i = "#"
                    if rule == example:
                        self.table_action[(q_ind, a)].add("a")
            # GOTO
            for A in self.first.keys():
                self.table_goto[(q_ind, A)] = goto_transitions[(q_ind, A)]

        # check for LR(1)
        for q_ind in range(len(Q)):
            for a in self.terminals | {"#"}:
                if len(self.table_action[(q_ind, a)]) > 1:
                    raise Exception("Grammar is not LR(1)")

        # print tables
        if DEBUG:
            lterminals = list(self.terminals)
            lnonterminals = list(self.first.keys())
            print("TABLES")
            print("ACTION | GOTO")
            for lett in lterminals:
                print(lett, end="       ")
            for lett in lnonterminals:
                print(lett, end="       ")
            print("")
            for ind in range(len(Q)):
                for lett in lterminals + ["#"]:
                    print(self.table_action[(ind, lett)], end="    ")
                for lett in lnonterminals:
                    print(self.table_goto[(ind, lett)], end="    ")
                print("")

    def checkLR1(self, text):
        for letter in text:
            if letter not in self.terminals:
                raise Exception(f"checkLR1: unexpected symbol {letter}")
        text += "#"
        stack = [0]
        pos = 0
        while pos < len(text):
            next_symbol = text[pos]
            cur_state = stack[-1]
            action = self.table_action[(cur_state, next_symbol)]
            if len(action) == 0:
                # nothing to do, reject
                return False
            action = list(action)[0]
            if action[0] == "s":
                # shift: read next symbol
                stack.append(next_symbol)
                stack.append(int(action[1:]))
                pos += 1
            elif action[0] == "r":
                # reduce: apply rule and pop from stack
                to_cut = len(self.rules[int(action[1:])].word)
                if to_cut != 0:
                    stack = stack[0:-2 * to_cut]
                next_state = stack[-1]
                A = self.rules[int(action[1:])].letter
                if self.table_goto[(next_state, A)] == -1:
                    return False
                stack.append(A)
                stack.append(self.table_goto[(next_state, A)])
            elif action == "a":
                # accept
                return True
            else:
                raise Exception("checkLR1: unknown action")
        raise Exception("checkLR1: end of fucntion reached")
