# LR1 parser


## Contents


Run ./test.sh to get test coverage


Run python3 main.py to start user input.

Input amount of rules in grammar, then rules in format:

"LETTER->SOME_TEXT" (f. e. "A->BCa+D") without quotes, then input text to be analized.

Right part must not be empty!

Non-terminals are A-Z. Don't use $ and # in both rules and text. Main rule is going to be $->S


File ContextFreeGrammar.py contains main ContextFreeGrammar class and some dependent classes


## How it works


1) create grammar from rules

2) set epsylon[nonterminal] = True <=> nonterminal->emty_string

3) set First array

4) find all terminals in rules

5) fill tables ACTION and GOTO:

    5.a) inititalise all states (Q)

    5.b) set goto_transitions[(i, a)] = j <=> goto(state[i], a) = statej

    5.c) fill ACTION for each pair (state_index, terminal) with SHIFT, REDUCE or ACCEPT

    5.d) fill GOTO using goto_transitions

    5.e) check for LR1 grammar by counting amount of rules in each ACTION cell

6) parse word:

    6.a) read word letter by letter and look at top of stack

    8.b) if ACTION[(current_state, letter)] is empty, reject

    8.c) if ACTION[(current_state, letter)] is reduce, apply rule

    8.d) if ACTION[(current_state, letter)] is shift, push stack and read next letter


## TODO

return parsing

LR(K)
