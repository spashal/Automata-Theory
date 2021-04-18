# Automata-Theory
A set of codes which can play with automata and do stuff like minimize a DFA, convert NFA to DFA etc. 

All codes to be run as ```python3 main.py input.json output.json``` where input.json should be in correct format. The folders have sample inp.json files.

### 1. Converting Regular Expression to NFA
The working logic of the code is
- Start parsing the regex from left to right
- The preference order to follow is '()' first followed by concatenate ('*') and + with the least priority
- We break the expression into smaller expressions separated by +, * or brackers and then convert the smaller expressions to their NFAs before joining these different NFAs with epsilon-transitions

### 2. NFA converted to an equivalent DFA
It is always possible to convert NFA into a DFA. This operation is crucial to help implement an NFA as a machine. How the code works:
- Currently the code can only handle NFAs with single start states
- We start out by creating a power-set of combination of states in the NFA. Therefore the DFA has 2 power n states
- We then traverse each set of states using the transitions of the member NFA-states. Since we can use the whole power-set, any transition can only take us to a state that is available
Note: The DFA obtained is very suboptimal and has a lot of useless transitions and unreachable states. We will use the 4th code to get an optimal DFA representative.

### 4. Minimizing the DFA
This code minimizes the DFA in terms of the number of states involved. The steps involved are:
- To remove unreachable states, we run a simple DFS with the starting state as root and mark every visited state so that unmarked ones can be discarded
- Divide the remaining states to 2 sets where one set contains all final states and one contains otherwise
- Have iterations to divide sets if possible on that basis of distinguishability and stop iterating when the number of sets and their constituents don't change
- Remember to output the new states as the formed sets (each set is a new state) and new transition functions and final states

## Thanks for reading! 
