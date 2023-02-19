# test

"""
# test insert command

list_one = [1, 2, 3]
list_two = [1, 2]

list_two.insert(2, list_one[2])

print(list_two)

if list_two == list_one:
    print('equal')
"""
"""
# test pop command

list_one = [1, 2, 3]

list_one.pop(2)
list_one.pop(1)

print(list_one)
"""
"""
# test remove

list_one = [1, 2, 3, 4]

list_one.remove(list_one[3])
list_one.remove(list_one[2])

print(list_one)
"""
"""
# create the present information list
# create the future choice list
# compare lists

# present information list merge x and y coordinate
# store future choice list in variable and flatten list to a long single list

# create a blank list to create the comparison future choice list

# create a variable to store the first three numbers of the long flattened future choice list from 0-2, left to right
# in order

# first two numbers will be put into a list to compare with present information list

# third number will be stored in a variable

# first three numbers will be removed from the list with *.remove() command and flattened list will be shorted the first
# future choice list

# the two lists will be compared with an if statement for a match and if successful the stored action key in variable
# will be returned and used for agent action

# if the two lists do not match then the same process will repeat of creating a future choice list to match until
# the list is empty of a match is made

# test multiple list comparison with single list
test_list = [1, 2]
agent_mario_future_comparison = [[4, 5, 6], [1, 2, 3], [4, 5, 6]]

# flatten future choice list
agent_mario_future_comparison = [i for j in agent_mario_future_comparison for i in j]

# loop iteration number to scan through whole future choice list until match or list finished
while_loop_iteration_number = int(len(agent_mario_future_comparison) / 3)

# create blank future comparison list and counter variables
future_comparison_list = []
i_iteration = 0
j_iteration = 0
agent_action_stored = 0

print(agent_mario_future_comparison)

# create nested loop to create and compare future information lists with present information list
while i_iteration < while_loop_iteration_number:
    i_iteration += 1
    # compare lists
    if future_comparison_list == test_list:
        agent_action = agent_action_stored
        # reset list for testing if works and break loop
        future_comparison_list = []
        print('\n', 'works')
        break
    else:
        future_comparison_list = []
    while j_iteration < 3:
        j_iteration += 1
        # create future list to compare with presesnt list
        if j_iteration != 3:
            future_comparison_list.append(agent_mario_future_comparison[0])
            agent_mario_future_comparison.remove(agent_mario_future_comparison[0])
            print(future_comparison_list, 'temporay future compare list')
            print(agent_mario_future_comparison, 'flattened future list')
        # reset counter and store agent action from list
        if j_iteration == 3:
            j_iteration = 0
            agent_action_stored = agent_mario_future_comparison[0]
            agent_mario_future_comparison.remove(agent_mario_future_comparison[0])
            print(agent_action_stored, 'agent action stored')
            break


print(while_loop_iteration_number, 'number of lists in future choice text file')
"""

# test removing duplicates from list
with open('AgentMarioFutureChoices.txt', 'r', encoding='utf-8') as future_choice_string:
    future_choice_integer = future_choice_string
    future_choice_integer = [eval(i) for i in future_choice_integer]
    future_choice_string.close()

print(len(future_choice_integer))

# future_choice_integer = [*set(future_choice_integer)]

# future_choice_integer = list(set(future_choice_integer))

future_choice_duplicates_removed = []
[future_choice_duplicates_removed.append(i) for i in future_choice_integer if i not in future_choice_duplicates_removed]

print(len(future_choice_duplicates_removed))

print(future_choice_duplicates_removed)

# res = []
# [res.append(x) for x in test_list if x not in res]

# l = [1, 2, 4, 2, 1, 4, 5]
# l = [*set(l)]
# print(l)

#test