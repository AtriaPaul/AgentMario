"""
Agent Notepad Mario
"""

from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
# from gym_super_mario_bros.actions import RIGHT_ONLY
# from gym_super_mario_bros.actions import COMPLEX_MOVEMENT
from gym_super_mario_bros.actions import JUMP_RIGHT_ONLY
import numpy as np

# env = JoypadSpace(gym_super_mario_bros.make('SuperMarioBros2-v0'), RIGHT_ONLY)
# env = JoypadSpace(gym_super_mario_bros.make('SuperMarioBros-v0'), RIGHT_ONLY)
# env = JoypadSpace(gym_super_mario_bros.make('SuperMarioBros-v0'), COMPLEX_MOVEMENT)

# creating environment variable
env = JoypadSpace(gym_super_mario_bros.make('SuperMarioBros-v0'), JUMP_RIGHT_ONLY)
# the counter for training steps
i = 0
# compare past and present game time for agent mario to determine if stuck and if stuck jump
agent_mario_time_compare_counter = 0
agent_mario_time_compare = 0

# creating blank text files to prevent read error from file that does not exist
with open('AgentMarioFutureChoices.txt', 'w', encoding='utf-8') as create_text:
    create_text.close()
with open('AgentMarioPastMemories.txt', 'w', encoding='utf-8') as create_text:
    create_text.close()
with open('AgentMarioPresentInformation.txt', 'w', encoding='utf-8') as create_text:
    create_text.close()
with open('AgentMarioPastInformation.txt', 'w', encoding='utf-8') as create_text:
    create_text.close()
with open('AgentMarioPastInformationCounter.txt', 'w', encoding='utf-8') as create_text:
    create_text.write(str(1))
    create_text.close()
with open('AgentMarioIsStuckTimer.txt', 'w', encoding='utf-8') as create_text:
    create_text.close()
with open('AgentMarioPastMemoriesCounter.txt', 'w', encoding='utf-8') as create_text:
    create_text.write(str(0))
    create_text.close()
with open('AgentMarioMemoriesAction.txt', 'w', encoding='utf-8') as create_text:
    create_text.close()
with open('GameOver.txt', 'w', encoding='utf-8') as create_text:
    create_text.close()
with open('HighJumpCounter.txt', 'w', encoding='utf-8') as create_text:
    create_text.write(str(0))
    create_text.close()
with open('HighJumpActivated.txt', 'w', encoding='utf-8') as create_text:
    create_text.write(str(0))
    create_text.close()
with open('AgentMarioTrailingPastMemories.txt', 'w', encoding='utf-8') as create_text:
    create_text.write(str([0]))
    create_text.write('\n')
    create_text.write(str([1, 1, 1]))
    create_text.close()
with open('DuplicateCoordinatesRemoval.txt', 'w', encoding='utf-8') as create_text:
    create_text.close()
with open('AgentMarioDiedInHole.txt', 'w', encoding='utf-8') as create_text:
    create_text.write(str(-1))
    create_text.close()
with open('AgentMarioDiedInHoleCounter.txt', 'w', encoding='utf-8') as create_text:
    create_text.write(str(0))
    create_text.close()
with open('SmallLargeJumpChoice.txt', 'w', encoding='utf-8') as create_text:
    create_text.write(str(0))
    create_text.close()

# reset the environment to create a clean start
env.reset()

# agent mario training
while i < 100000:
    i += 1
    # for human to see the agent mario work
    env.render()

    # agent actions through the environment
    env.step(env.action_space.sample())

    """
    ***************
    test purpose
    ***************
    # using a list for agent mario present location and status
    with open('AgentMarioPresentInformation.txt', 'r', encoding='utf-8') as agent_mario_present_information_string:
        # pull information from text file into a variable
        agent_mario_present_information_integer = agent_mario_present_information_string

        # convert the string from notepad text file to an integer or float running through entire notepad text file
        agent_mario_present_information_integer_complete = [eval(i) for i in agent_mario_present_information_integer]

        # print(agent_mario_present_information_integer_complete[0]) # row one first set of list x position of agent mario
        # print(agent_mario_present_information_integer_complete[1]) # row two second set of list y position of agent mario
        # agent_mario_present_information_integer_complete[2] # row three third set of list mario died or alive, 11 died 8 alive
        # agent_mario_present_information_integer_complete[3] # row four world time

        # when agent mario hits 11 for dead the world timer still runs one second ahead and records as the stored
        # information when agent mario died in text file is 393 and the printed world time in pycharm is 392
        # the timer displayed on the screen in game is 393

        # if agent_mario_present_information_integer_complete[2] == 11:
            # print(agent_mario_present_information_integer_complete[2])
            # print(agent_mario_present_information_integer_complete[3])

    # close text file to allow continues writing to file
    agent_mario_present_information_string.close()
    """

    # agent marios past information several i while loop steps behind present information
    # check if the remainder after i divided by three is 0 then the number is odd
    # creates a past location information file for agent mario but is consistent three x locations behind in 100 step
    # while loop i step process because i starts at one then two and then three which is the first recording
    # even number divisible by two leads to duplicate past present agent mario information file
    # odd number modulus divided by three as the program returns the remainder divided by a number and if remainder is
    # zero then the number was divisible by that number with no remainder
    if (i % 3) == 0:
        with open('AgentMarioPastInformationCounter.txt', 'r', encoding='utf-8') as start_past_information_counter_string:
            start_past_information_counter_integer = start_past_information_counter_string
            start_past_information_counter_integer = [eval(i) for i in start_past_information_counter_integer]
            start_past_information_counter_string.close()

            # if the counter is not activated activate and add to counter
            if start_past_information_counter_integer[0] == 1:
                with open('AgentMarioPastInformationCounter.txt', 'a', encoding='utf-8') as start_past_information_counter_string:
                    start_past_information_counter_string.write(str(1))
                    start_past_information_counter_string.close()
            elif start_past_information_counter_integer[0] == 11:
                with open('AgentMarioPastInformationCounter.txt', 'a', encoding='utf-8') as start_past_information_counter_string:
                    start_past_information_counter_string.write(str(1))
                    start_past_information_counter_string.close()
            elif start_past_information_counter_integer[0] == 111:
                with open('AgentMarioPastInformationCounter.txt', 'a', encoding='utf-8') as start_past_information_counter_string:
                    start_past_information_counter_string.write(str(1))
                    start_past_information_counter_string.close()

        if start_past_information_counter_integer[0] == 1111:
            # start counter over
            with open('AgentMarioPastInformationCounter.txt', 'w', encoding='utf-8') as start_past_information_counter_string:
                start_past_information_counter_string.write(str(1))
                start_past_information_counter_string.close()

            # write the list file in multiple rows
            with open('AgentMarioPresentInformation.txt', 'r', encoding='utf-8') as agent_mario_present_information_string:
                agent_mario_past_information_string = agent_mario_present_information_string
                agent_mario_past_information_string_integer = [eval(i) for i in agent_mario_past_information_string]
                with open('AgentMarioPastInformation.txt', 'w', encoding='utf-8') as agent_mario_past_information_string_temp:
                    agent_mario_past_information_string_temp.write(str(agent_mario_past_information_string_integer[0]))
                    agent_mario_past_information_string_temp.write('\n')
                    agent_mario_past_information_string_temp.write(str(agent_mario_past_information_string_integer[1]))
                    agent_mario_past_information_string_temp.write('\n')
                    agent_mario_past_information_string_temp.write(str(agent_mario_past_information_string_integer[2]))
                    agent_mario_past_information_string_temp.write('\n')
                    agent_mario_past_information_string_temp.write(str(agent_mario_past_information_string_integer[3]))
                    agent_mario_past_information_string_temp.write('\n')
                    agent_mario_past_information_string_temp.write(str(agent_mario_past_information_string_integer[4]))
                    agent_mario_past_information_string_temp.close()

                    # close text file to allow continues reading/writing to file
                    agent_mario_present_information_string.close()

    # determine is agent mario is stuck and if stuck record in text file agent mario needs to jump
    # using x location of agent mario to determine if agent mario is stuck as past time will never equal future time
    with open('AgentMarioPresentInformation.txt', 'r', encoding='utf-8') as agent_mario_present_information_string:
        agent_mario_present_information_integer = agent_mario_present_information_string
        agent_mario_present_information_integer = [eval(i) for i in agent_mario_present_information_integer]
        agent_mario_present_information_string.close()

    agent_mario_time_compare_counter += 1
    # in row [3] the information is an integer as 400 example
    # in row 3, line 4 [3:4] the information is in a list as [400] as example
    agent_mario_present_information_integer_timer = agent_mario_present_information_integer[0]

    # reset action keys to take new action for agent mario after completing a full jump
    if agent_mario_time_compare_counter == 15:
        with open('AgentMarioIsStuckTimer.txt', 'w', encoding='utf-8') as activate_jump:
            activate_jump.write(str(0))
            activate_jump.close()

    if agent_mario_time_compare_counter == 50:
        # reset counter to always check agent mario stuck every 50 program cycles
        agent_mario_time_compare_counter = 0
        # compare past and present timers for agent mario to determine is stuck
        if agent_mario_time_compare == agent_mario_present_information_integer_timer:
            # record to text file agent mario needs to jump
            # print(agent_mario_present_information_integer_timer, 'present timer')
            # print(agent_mario_time_compare, 'past timer')
            with open('AgentMarioIsStuckTimer.txt', 'w', encoding='utf-8') as activate_jump:
                activate_jump.write(str(1))
                activate_jump.close()

            agent_mario_stuck_jump = [agent_mario_present_information_integer[0], agent_mario_present_information_integer[1], 1]

            with open('AgentMarioFutureChoices.txt', 'a', encoding='utf-8') as future_choice_string:
                future_choice_string.write(str(agent_mario_stuck_jump))
                future_choice_string.write('\n')

        else:
            agent_mario_time_compare = agent_mario_present_information_integer_timer

    # future list duplicate removal
    i_iteration = int(0)
    j_iteration = int(0)
    future_choice_duplicates_removed = []
    future_choice_build_list = []

    # record information out of the future choice file
    with open('AgentMarioFutureChoices.txt', 'r', encoding='utf-8') as remove_duplicates_string:
        remove_duplicates_integer = remove_duplicates_string
        remove_duplicates_integer = [eval(i) for i in remove_duplicates_integer]
        remove_duplicates_string.close()

    # remove duplicates in the futures list keeping list in order
    [future_choice_duplicates_removed.append(i) for i in remove_duplicates_integer if i not in future_choice_duplicates_removed]
    # print(future_choice_duplicates_removed, 'duplicates build list removed')
    # flatten list to remove nested lists and prevent building nested lists inside nested lists each
    # program i cycle causing crash
    future_choice_duplicates_removed = [i for j in future_choice_duplicates_removed for i in j]
    # print(future_choice_duplicates_removed, 'duplicates build list flattened')
    # how many times the for while loop will run to build the futures list
    futures_choice_list_length = int(len(future_choice_duplicates_removed) / 3)
    # print(futures_choice_list_length, 'while iteration build list length')

    # erase file to prepare to create a future list free from duplicates
    with open('AgentMarioFutureChoices.txt', 'w', encoding='utf-8') as erase_text_file:
        erase_text_file.write(str([1, 1, 1]))
        erase_text_file.write('\n')
        erase_text_file.close()

    # write the future choices back to text file
    while i_iteration < futures_choice_list_length:
        i_iteration += 1
        while j_iteration <= 3:
            j_iteration += 1
            if j_iteration <= 3:
                future_choice_build_list.append(future_choice_duplicates_removed[0])
                future_choice_duplicates_removed.remove(future_choice_duplicates_removed[0])
                # print(future_choice_build_list, 'build list created')
            if j_iteration == 4:
                j_iteration = 0
                # print(future_choice_build_list, 'build list appended to file')
                with open('AgentMarioFutureChoices.txt', 'a', encoding='utf-8') as duplicates_removed_test_string:
                    duplicates_removed_test_string.write(str(future_choice_build_list))
                    duplicates_removed_test_string.write('\n')
                    duplicates_removed_test_string.close()
                future_choice_build_list = []
                break

    # print(future_choice_duplicates_removed, 'list removed')

    """
    # trailing memories file to use in case agent mario gets stuck on
    # short fall deaths into or jumping into an enemy then dies and can not get out of loop
    # because an agent mario action can not be executed while jumping or falling in mid air except right left commands
    # check futures file for duplicate x y coordinates
    # then move agent mario agent action back approximately 64 x coordinates from past memories location
    # or 4 square tiles the time it takes to walk off a ledge and fall into an enemy and die getting stuck in loop
    i2_iteration = int(0)
    j2_iteration = int(0)
    x_y_duplicate_comparison_list = []
    x_duplicate_comparison_list = []
    y_duplicate_comparison_list = []
    x_compare = []
    y_compare = []

    with open('AgentMarioFutureChoices.txt', 'r', encoding='utf-8') as duplicates_string:
        duplicates_integer = duplicates_string
        duplicates_integer = [eval(i) for i in duplicates_integer]
        duplicates_string.close()

    # flatten list for list length to measure how many while loop cycles and create a x y list to compare
    # with past memories x y location
    x_y_duplicate_list = [i for j in duplicates_integer for i in j]
    # print(x_y_duplicate_list, 'original')

    # make another duplicate list for comparison as first is chopped up and extracted for comparison
    x_y_duplicate_list_for_comparison = [i for j in duplicates_integer for i in j]
    # x_y_duplicate_list_for_comparison = [1, 1]
    # print(x_y_duplicate_list_for_comparison, 'duplicate for list comparison')
    # print(x_y_duplicate_list_for_comparison[0], 'duplicate for list comparison [0]')

    # get list length
    x_y_duplicate_list_length = int(len(x_y_duplicate_list) / 3)
    # print(x_y_duplicate_list_length, 'x y duplicate list length')

    # erase file to prepare to create a duplicate list text file
    with open('DuplicateCoordinatesRemoval.txt', 'w', encoding='utf-8') as erase_text_file:
        erase_text_file.write(str([1, 1]))
        erase_text_file.write('\n')
        erase_text_file.close()

    
    problem is the the comparison file for duplicate matches as the x y for duplicate file always will match with the
    x y duplicate file as only the first file is chopped down and the second is the original equaling a logic error
    causing the file to always find a match and not find duplicate matches only
    
    *logic error must be corrected first before moving on to erasing x y duplicates and rebuilding a futures.txt file
    with previous four squares location to break loop and without x y duplicates
    
    

    while i2_iteration < x_y_duplicate_list_length:
        i2_iteration += 1
        while j2_iteration < 3:
            j2_iteration += 1
            x_y_duplicate_comparison_list.append(x_y_duplicate_list[0])
            x_y_duplicate_list.remove(x_y_duplicate_list[0])
            # print(x_y_duplicate_list, 'duplicate list build compare')
            # print(x_y_duplicate_list_for_comparison, 'duplicate list build compare for')
            if j2_iteration == 3:
                # remove the first list so the file does not compare with a list that would register as a
                # false duplicate
                if i2_iteration != 1:
                    x_y_duplicate_list_for_comparison.remove(x_y_duplicate_list_for_comparison[2])
                    x_y_duplicate_list_for_comparison.remove(x_y_duplicate_list_for_comparison[1])
                    x_y_duplicate_list_for_comparison.remove(x_y_duplicate_list_for_comparison[0])
                j2_iteration = 0
                # print(x_y_duplicate_comparison_list, 'duplicate build list')
                # remove agent mario action from x y duplicate list to compare
                x_y_duplicate_comparison_list.remove(x_y_duplicate_comparison_list[2])
                # print(x_y_duplicate_comparison_list, 'duplicate build list agent action removed')
                # create separate x y for comparison with rest of list to find matches
                x_duplicate_comparison_list.append(x_y_duplicate_comparison_list[0])
                # x_y_duplicate_comparison_list.remove(x_y_duplicate_comparison_list[0])
                y_duplicate_comparison_list.append(x_y_duplicate_comparison_list[1])
                x_y_duplicate_comparison_list = []
                # print(x_duplicate_comparison_list, 'x')
                # print(y_duplicate_comparison_list, 'y')
                # print(x_y_duplicate_list, 'duplicate list after append remove')
                # print(x_y_duplicate_list_for_comparison)
                x_compare = x_duplicate_comparison_list[0]
                y_compare = y_duplicate_comparison_list[0]
                # temporary as the x y lists need to be reset to not produce wrong data
                x_duplicate_comparison_list = []
                y_duplicate_comparison_list = []
                # print(x_compare, 'x compare')
                # print(y_compare, 'y compare')
                # print(x_y_duplicate_list_for_comparison)
                # x_y_duplicate_list = [1, 1]
                # scan list for duplicate x y
                variable = 0
                while variable < x_y_duplicate_list_length:
                    if x_compare == x_y_duplicate_list_for_comparison[variable]:
                        if y_compare == x_y_duplicate_list_for_comparison[variable + 1]:
                            # write text file x y duplicate coordinates to remove those duplicates of failed
                            # agent mario actions getting stuck in a loop
                            with open('DuplicateCoordinatesRemoval.txt', 'a', encoding='utf-8') as duplicate_x_y_removal_string:
                                duplicate_x_y_removal_string.write(str([x_compare, y_compare]))
                                duplicate_x_y_removal_string.write('\n')
                                duplicate_x_y_removal_string.close()
                            # give agent mario approximately four squares back for new agent action to break stuck loop
                            x_compare = x_compare - 64
                            # create new agent mario list for future text file
                            new_agent_mario_action = [x_compare, y_compare, np.random.random_integers(0, 4)]
                            # print(new_agent_mario_action, 'new random agent mario action')
                            # print(x_compare)
                            # print('working', '\n')
                            # if x compare is greater than 0 append future text file
                            # with new coordinates and agent action as the default [1, 1, 1] is set up to prevent
                            # program crash also x will come out to -63 and does not need to burden the file
                            if x_compare > 0:
                                with open('AgentMarioFutureChoices.txt', 'a', encoding='utf-8') as append_choice_string:
                                    append_choice_string.write(str(new_agent_mario_action))
                                    append_choice_string.write('\n')
                                    append_choice_string.close()
                            break
                    variable += 1
                break
    """
    # remove duplicates after a time period as the new agent action from getting stuck will overburden the file
    # with many more choices if the duplicates are not removed again as first duplicate removes duplicates from
    # x y and agent action match
    # getting stuck while loop looks for duplicates from x y and makes a choice previous to the x location
    # creating more duplicates from x y and different agent actions to a total of 5 different file append locations
    # the duplicate x y locations will be removed leaving the [x - 64, y, random mario agent action] choice as duplicate
    # x y is no longer needed

    """
    *******************************
    plan
    *******************************
    
    *take duplicate x y list and compare it to future file list looking for match of x y
    *build future file list without the duplicate x y lists
    *
    
    
    """

    """
    i3_iteration = int(0)
    j3_iteration = int(0)
    x_y_duplicate_comparison_list2 = []
    x_duplicate_comparison_list2 = []
    y_duplicate_comparison_list2 = []
    x_compare2 = []
    y_compare2 = []

    with open('AgentMarioFutureChoices.txt', 'r', encoding='utf-8') as duplicates_string2:
        duplicates_integer2 = duplicates_string2
        duplicates_integer2 = [eval(i) for i in duplicates_integer2]
        duplicates_string2.close()

    # flatten list for list length to measure how many while loop cycles and create a x y list to compare
    # with past memories x y location
    x_y_duplicate_list = [i for j in duplicates_integer for i in j]
    # print(x_y_duplicate_list, 'original')

    # make another duplicate list for comparison as first is chopped up and extracted for comparison
    x_y_duplicate_list_for_comparison = [i for j in duplicates_integer for i in j]
    # x_y_duplicate_list_for_comparison = [1, 1]
    # print(x_y_duplicate_list_for_comparison, 'duplicate for list comparison')
    # print(x_y_duplicate_list_for_comparison[0], 'duplicate for list comparison [0]')

    # get list length
    x_y_duplicate_list_length = int(len(x_y_duplicate_list) / 3)
    # print(x_y_duplicate_list_length, 'x y duplicate list length')

    # erase file to prepare to create a duplicate list text file
    with open('DuplicateCoordinatesRemoval.txt', 'w', encoding='utf-8') as erase_text_file:
        erase_text_file.write(str([1, 1]))
        erase_text_file.write('\n')
        erase_text_file.close()

    while i2_iteration < x_y_duplicate_list_length:
        i2_iteration += 1
        while j2_iteration < 3:
            j2_iteration += 1
            x_y_duplicate_comparison_list.append(x_y_duplicate_list[0])
            x_y_duplicate_list.remove(x_y_duplicate_list[0])
            # print(x_y_duplicate_list, 'duplicate list build compare')
            # print(x_y_duplicate_list_for_comparison, 'duplicate list build compare for')
            if j2_iteration == 3:
                j2_iteration = 0
                # print(x_y_duplicate_comparison_list, 'duplicate build list')
                # remove agent mario action from x y duplicate list to compare
                x_y_duplicate_comparison_list.remove(x_y_duplicate_comparison_list[2])
                # print(x_y_duplicate_comparison_list, 'duplicate build list agent action removed')
                # create separate x y for comparison with rest of list to find matches
                x_duplicate_comparison_list.append(x_y_duplicate_comparison_list[0])
                # x_y_duplicate_comparison_list.remove(x_y_duplicate_comparison_list[0])
                y_duplicate_comparison_list.append(x_y_duplicate_comparison_list[1])
                x_y_duplicate_comparison_list = []
                # print(x_duplicate_comparison_list, 'x')
                # print(y_duplicate_comparison_list, 'y')
                # print(x_y_duplicate_list, 'duplicate list after append remove')
                # print(x_y_duplicate_list_for_comparison)
                x_compare = x_duplicate_comparison_list[0]
                y_compare = y_duplicate_comparison_list[0]
                # temporary as the x y lists need to be reset to not produce wrong data
                x_duplicate_comparison_list = []
                y_duplicate_comparison_list = []
                # print(x_compare, 'x compare')
                # print(y_compare, 'y compare')
                # print(x_y_duplicate_list_for_comparison)
                # x_y_duplicate_list = [1, 1]
                # scan list for duplicate x y
                variable = 0
                while variable < x_y_duplicate_list_length:
                    if x_compare == x_y_duplicate_list_for_comparison[variable]:
                        if y_compare == x_y_duplicate_list_for_comparison[variable + 1]:
                            # write text file x y duplicate coordinates to remove those duplicates of failed
                            # agent mario actions getting stuck in a loop
                            with open('DuplicateCoordinatesRemoval.txt', 'a', encoding='utf-8') as duplicate_x_y_removal_string:
                                duplicate_x_y_removal_string.write(str([x_compare, y_compare]))
                                duplicate_x_y_removal_string.write('\n')
                                duplicate_x_y_removal_string.close()
                            # give agent mario approximately four squares back for new agent action to break stuck loop
                            x_compare = x_compare - 64
                            # create new agent mario list for future text file
                            new_agent_mario_action = [x_compare, y_compare, np.random.random_integers(0, 4)]
                            # print(new_agent_mario_action, 'new random agent mario action')
                            # print(x_compare)
                            # print('working', '\n')
                            # if x compare is greater than 0 append future text file
                            # with new coordinates and agent action as the default [1, 1, 1] is set up to prevent
                            # program crash also x will come out to -63 and does not need to burden the file
                            if x_compare > 0:
                                with open('AgentMarioFutureChoices.txt', 'a', encoding='utf-8') as append_choice_string:
                                    append_choice_string.write(str(new_agent_mario_action))
                                    append_choice_string.write('\n')
                                    append_choice_string.close()
                            break
                    variable += 1
                break
    """

env.close()

# example code given in gym super mario brothers download
"""
done = True
for step in range(100):
    if done:
        state = env.reset()
    state, reward, done, info = env.step(env.action_space.sample())

    env.render()

env.close()
"""

