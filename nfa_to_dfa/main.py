import json
import sys
import ast

with open(sys.argv[1], 'r') as file:
    data = json.load(file)
data = ast.literal_eval(json.dumps(data))

t_fun = data['transition_function']
letters = data['letters']
states = []
states = data["states"]
start_states = data['start_states']
final_states = data['final_states']
state_index = {}
new_t_fun = []
subset = []
new_final_states = []

for i in range(len(states)):
    state_index.update({states[i]: i})

max_states = 1 << len(states)

subset.append([])
for i in range(max_states):
    subset.append([])
    for j in range(len(states)):
        if i & 1 << j:
            subset[i].append(states[j])
    for j in range(len(letters)):
        union = []
        for k in range(len(states)):
            if i & 1 << k:
                for l in range(len(t_fun)):
                    if state_index[t_fun[l][0]] == k and letters[j] == t_fun[l][1]:
                        if t_fun[l][2] not in union:
                            union.append(t_fun[l][2])
                    # get the transition for each state in i if it exists and take union
        new_t_fun.append([subset[i], letters[j], list(union)])

for i in range(max_states):
    should_break = False
    for j in range(len(subset[i])):
        for k in range(len(final_states)):
            if subset[i][j] == final_states[k]:
                should_break = True
                new_final_states.append(subset[i])
                break
        if should_break:
            break


json_out = {}
json_out['states'] = subset
json_out['letters'] = data['letters']
json_out['transition_function'] = new_t_fun
json_out['start_states'] = data['start_states']
json_out['final_states'] = new_final_states

with open(sys.argv[2], 'w') as write_file:
    json.dump(json_out, write_file, indent=1)
