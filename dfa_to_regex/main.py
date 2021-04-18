import json, sys

with open(sys.argv[1], 'r') as file:
    data = json.load(file)

t_fun = data['transition_function']
letters = data['letters']
states = data['states']
state_index = {}
regex = ['' for i in range(len(states))]
on = [False for i in range(len(states))]

for i in range(len(states)):
    state_index[states[i]] = i

edge = [[] for i in range(len(states))]
print(edge)


for i in range(len(t_fun)):
    edge[state_index[t_fun[i][0]]].append((t_fun[i][1], state_index[t_fun[i][2]]))


def dfs_for_nfa_to_dfa(node):
    if on[node]:
        return node, ''
    global edge, states
    str = []
    final = '('
    on[node] = True
    for i in range(len(edge[node])):
        str.append([])
        final += edge[node][i][0]
        str.append(dfs_for_nfa_to_dfa(edge[node][i][1]))

    temp_str = ' ('
    for i in range(len(edge[node])):
        if str[i][0] == node:
            temp_str += str[i][1]
    temp_str += ')*'
    final = temp_str
    for i in range(len(edge[node])):
        if str[i][0] == -1:
            final += ' + ' + str[i][1]
    final += ') '
    on[node] = False
    return -1, final


dfs_for_nfa_to_dfa(state_index[data['start_states'][0]], '')
