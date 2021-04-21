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
reachable = [False for i in range(len(states))]
on = [False for i in range(len(states))]
state_index = {}


def give_states_index(state):
    for i in range(len(states)):
        if states[i] == state:
            return i
    return 0


def give_letters_index(letter):
    for i in range(len(letters)):
        if letters[i] == letter:
            return i
    return 0


def mark_reachable(state):
    if on[state]:
        return
    reachable[state] = True
    on[state] = True
    for i in range(len(t_fun)):
        if t_fun[i][0] == states[state]:
            mark_reachable(give_states_index(t_fun[i][2]))
    on[state] = False


mark_reachable(give_states_index([start_states[0]]))

minimized_states = []
for i in range(len(states)):
    if reachable[i]:
        minimized_states.append(states[i])

sets = [[], []]
print(final_states)
print(states)
for i in minimized_states:
    is_it_final = False
    for j in final_states:
        if i == j:
            if i not in sets[0] and i != []:
                sets[0].append(i)
            is_it_final = True
            break
    if not is_it_final:
        if i not in sets[1] and i != []:
            sets[1].append(i)

temp_set = []
set_t_funs = [[] for i in range(2)]
while temp_set != sets:
    temp_set = sets
    set_t_funs = [[] for i in range(len(sets))]
    set_len = len(sets)
    for i in range(set_len):
        partition = [[-1 for m in range(len(letters))] for j in range(len(sets[i]))]
        for j in range(len(sets[i])):
            for m in range(len(t_fun)):
                if t_fun[m][0] == sets[i][j]:
                    for n in range(len(sets)):
                        if t_fun[m][2] in sets[n]:
                            partition[j][give_letters_index(t_fun[m][1])] = n
        did_append = False
        set_len_temp = len(sets[i])
        for j in range(1, len(sets[i])):
            set_t_funs[i] = partition[j]
            for m in range(len(letters)):
                if partition[0][m] != partition[j][m]:
                    if did_append:
                        print(sets[i][j])
                        sets[len(sets) - 1].append(sets[i][j])
                        sets[i].pop(j)
                        j -= 1
                    else:
                        did_append = True
                        sets.append([sets[i][j]])
                        set_t_funs.append([partition[j]])
                        sets[i].pop(j)
                        j -= 1
        if did_append:
            break

new_final_states = []
for i in range(len(sets)):
    for j in range(len(final_states)):
        if final_states[j] in sets[i]:
            new_final_states.append(sets[i])
            break

new_t_fun = []
for i in range(len(sets)):
    for j in range(len(letters)):
        for k in range(len(t_fun)):
            if t_fun[k][0] in sets[i] and t_fun[k][1] == letters[j]:
                for m in range(len(sets)):
                    if t_fun[k][2] in sets[m]:
                        new_t_fun.append([sets[i], letters[j], sets[m]])
                break

json_out = {}
index = []
for i in sets:
    if start_states[0] in i:
        index.append(i)
        break

json_out['states'] = sets
json_out['letters'] = letters
json_out['transition_function'] = new_t_fun
json_out['start_states'] = index
json_out['final_states'] = new_final_states

with open(sys.argv[2], 'w') as write_file:
    json.dump(json_out, write_file, indent=1)
