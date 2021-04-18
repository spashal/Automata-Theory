# shuru karo antakshari leke prabhu ka naaaaaM
import json, sys

with open(sys.argv[1], 'r') as read_file:
    regex = json.load(read_file)
    regex = regex['regex']

no_of_nodes = 0
transitions = []
json_out = {}
output = []
states = []
letters_temp = []


def assign_node():
    global no_of_nodes
    no_of_nodes += 1
    transitions.append([])
    states.append(('q{}'.format(no_of_nodes - 1)))
    return no_of_nodes - 1


def give_nfa(expression, start, end):
    global no_of_nodes, transitions
    if start == -1:
        start = assign_node()
    if end == -1:
        end = assign_node()
    prev_start = 0
    prev_end = 0
    global no_of_nodes, transitions
    cur = start
    i = 0
    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        if expression[i] == '(':
            temp_end = 0
            ctr = 1
            for j in range(i + 1, len(expression)):
                if expression[j] == '(':
                    ctr += 1
                if expression[j] == ')':
                    ctr -= 1
                    if ctr == 0:
                        temp_end = j
                        break
            prev_start, prev_end = give_nfa(expression[i+1:temp_end], cur, -1)
            cur = prev_end
            i = temp_end

        elif expression[i] == '+':
            give_nfa(expression[i+1:], start, end)
            break

        elif expression[i] == '*':
            if prev_start != prev_end:
                transitions[prev_start].append(['$', prev_end])
                transitions[prev_end].append(['$', prev_start])
            else:
                transitions[cur].append([expression[i-1], cur])

        else:
            # prev_parent = cur
            letters_temp.append(expression[i])
            if i + 1 < len(expression) and expression[i + 1] == '*':
                i += 1
                continue
            prev_end = cur
            prev_start = cur
            new_node = assign_node()
            transitions[cur].append([expression[i], new_node])
            cur = new_node

        i += 1

    transitions[cur].append(['$', end])
    return start, end


give_nfa(regex, -1, -1)
start = 0

for i in range(0, no_of_nodes):
    for j in range(len(transitions[i])):
        output.append(('q{}'.format(i), transitions[i][j][0], 'q{}'.format(transitions[i][j][1])))

new_final_states = ['q1']
temp = [1]
while len(temp) > 0:
    for i in range(len(transitions)):
        for j in range(len(transitions[i])):
            if transitions[i][j][1] == temp[0] and transitions[i][j][0] == '$':
                if ('q{}'.format(i)) not in new_final_states:
                    new_final_states.append(('q{}'.format(i)))
                    temp.append(i)
    temp.pop(0)


letters = []
for i in letters_temp:
    if i not in letters:
        letters.append(i)

json_out['states'] = states
json_out['letters'] = letters
json_out['transition_function'] = output
json_out['start_states'] = ['q0']
json_out['final_states'] = new_final_states
with open(sys.argv[2], 'w') as write_file:
    json.dump(json_out, write_file, indent=1)
