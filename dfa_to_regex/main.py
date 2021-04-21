# lets aksilerate
import json
import sys
import ast

with open(sys.argv[1], 'r') as file:
    data = json.load(file)
data = ast.literal_eval(json.dumps(data))

states = data['states']
t_fun = data['transition_function']
start_states = data['start_states']
final_states = data['final_states']
letters = data['letters']

# converting dfa to gnfa
states.append('qs')
states.append('qf')
for i in range(len(start_states)):
    t_fun.append(["qs", "$", start_states[i]])
for i in range(len(final_states)):
    t_fun.append([final_states[i], "$", "qf"])


def remove_node(state):
    global states, t_fun
    # select node to remove

    # make new transitions before removal, remember to put brackets for safety
    has_self_edge = False
    self_edge_exp = '$'
    ctr1 = 0
    for i in range(len(t_fun)):
        if t_fun[i][0] == t_fun[i][2] == state:
            ctr1 += 1
    while ctr1:
        for i in range(len(t_fun)):
            if t_fun[i][0] == t_fun[i][2] == state:
                has_self_edge = True
                self_edge_exp += '+' + t_fun[i][1]
                t_fun.pop(i)
                break
        ctr1 -= 1

    self_edge_exp = '(' + self_edge_exp + ')'

    for a in t_fun:
        if a[2] == state:
            for b in t_fun:
                if b[0] == state:
                    temp = ''
                    for c in range(len(t_fun)):
                        if t_fun[c][0] == a[0] and t_fun[c][2] == b[2]:
                            temp = t_fun[c][1]
                            t_fun.pop(c)
                            break
                    exp = ''
                    if a[1] != '$':
                        exp = a[1]
                    if has_self_edge and self_edge_exp != '$':
                        exp += self_edge_exp + "*"
                    if b[1] != '$':
                        exp += b[1]

                    # add already existing edge between connected nodes
                    if temp != '':
                        temp2 = exp
                        exp = '(' + temp2 + '+' + temp + ')'
                    t_fun.append([a[0], exp, b[2]])

                    # removing the constituent edges

    ctr = 0
    for i in range(len(t_fun)):
        if t_fun[i][0] == state or t_fun[i][2] == state:
            ctr += 1
    while ctr:
        ctr -= 1
        for i in range(len(t_fun)):
            if t_fun[i][0] == state or t_fun[i][2] == state:
                t_fun.pop(i)
                break

    return


while len(states) > 2:
    for i in range(len(states)):
        if states[i] != 'qf' or states[i] != 'qs':
            remove_node(states[i])
            states.pop(i)
            break

output = {}
output['regex'] = t_fun[0][1]
with open(sys.argv[2], 'w') as write_file:
    json.dump(output, write_file, indent=1)

