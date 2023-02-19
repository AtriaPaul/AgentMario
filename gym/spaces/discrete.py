"""Implementation of a space consisting of finitely many elements."""
import random
from typing import Optional, Union

import numpy as np
from gym.spaces.space import Space


class Discrete(Space[int]):
    r"""A space consisting of finitely many elements.

    This class represents a finite subset of integers, more specifically a set of the form :math:`\{ a, a+1, \dots, a+n-1 \}`.

    Example::

        >>> Discrete(2)            # {0, 1}
        >>> Discrete(3, start=-1)  # {-1, 0, 1}
    """

    def __init__(
        self,
        n: int,
        seed: Optional[Union[int, np.random.Generator]] = None,
        start: int = 0,
    ):
        r"""Constructor of :class:`Discrete` space.

        This will construct the space :math:`\{\text{start}, ..., \text{start} + n - 1\}`.

        Args:
            n (int): The number of elements of this space.
            seed: Optionally, you can use this argument to seed the RNG that is used to sample from the ``Dict`` space.
            start (int): The smallest element of this space.
        """
        assert isinstance(n, (int, np.integer))
        assert n > 0, "n (counts) have to be positive"
        assert isinstance(start, (int, np.integer))
        self.n = int(n)
        self.start = int(start)
        super().__init__((), np.int64, seed)

    @property
    def is_np_flattenable(self):
        """Checks whether this space can be flattened to a :class:`spaces.Box`."""
        return True

    def sample(self, mask: Optional[np.ndarray] = None) -> int:
        """Generates a single random sample from this space.

        A sample will be chosen uniformly at random with the mask if provided

        Args:
            mask: An optional mask for if an action can be selected.
                Expected `np.ndarray` of shape `(n,)` and dtype `np.int8` where `1` represents valid actions and `0` invalid / infeasible actions.
                If there are no possible actions (i.e. `np.all(mask == 0)`) then `space.start` will be returned.

        Returns:
            A sampled integer from the space
        """
        if mask is not None:
            assert isinstance(
                mask, np.ndarray
            ), f"The expected type of the mask is np.ndarray, actual type: {type(mask)}"
            assert (
                mask.dtype == np.int8
            ), f"The expected dtype of the mask is np.int8, actual dtype: {mask.dtype}"
            assert mask.shape == (
                self.n,
            ), f"The expected shape of the mask is {(self.n,)}, actual shape: {mask.shape}"
            valid_action_mask = mask == 1
            assert np.all(
                np.logical_or(mask == 0, valid_action_mask)
            ), f"All values of a mask should be 0 or 1, actual values: {mask}"
            if np.any(valid_action_mask):
                return int(
                    self.start + self.np_random.choice(np.where(valid_action_mask)[0])
                )
            else:
                return self.start

        # compare agent mario negative past memories results with future positive choices and present information
        # to decide course of action
        # if future choice choose future choice else choose past memories choice with different random choice for action
        # else choose random choice for action
        with open('AgentMarioFutureChoices.txt', 'r', encoding='utf-8') as agent_mario_future_choices_string:
            agent_mario_future_choices_integer = agent_mario_future_choices_string
            agent_mario_future_choices_integer = [eval(i) for i in agent_mario_future_choices_integer]
            agent_mario_future_choices_string.close()
        with open('AgentMarioPastMemories.txt', 'r', encoding='utf-8') as agent_mario_past_memories_string:
            agent_mario_past_memories_integer = agent_mario_past_memories_string
            agent_mario_past_memories_integer = [eval(i) for i in agent_mario_past_memories_integer]
            # print(agent_mario_past_memories_integer, 'value memories first')
            agent_mario_past_memories_string.close()
        with open('AgentMarioPresentInformation.txt', 'r', encoding='utf-8') as agent_mario_present_information_string:
            agent_mario_present_information_integer = agent_mario_present_information_string
            agent_mario_present_information_integer = [eval(i) for i in agent_mario_present_information_integer]
            # print(agent_mario_present_information_integer, 'value present first')
            agent_mario_present_information_string.close()
        with open('AgentMarioPastInformation.txt', 'r', encoding='utf-8') as agent_mario_past_information_string:
            agent_mario_past_information_integer = agent_mario_past_information_string
            agent_mario_past_information_integer = [eval(i) for i in agent_mario_past_information_integer]
            agent_mario_past_information_string.close()

        """
        # compare present and past timer information to know if agent mario is stuck in a location and needs to jump
        agent_mario_past_information_integer_timer = agent_mario_past_information_integer[3:4]
        print(agent_mario_past_information_integer_timer, 'past timer')
        agent_mario_present_information_integer_timer = agent_mario_present_information_integer[3:4]
        print(agent_mario_present_information_integer_timer, 'present timer')
        """

        # agent_mario_past_information_integer_x = agent_mario_past_information_integer[0:1]

        # make present information and memories list to compare x y coordinates
        agent_mario_present_information_integer_x = agent_mario_present_information_integer[0:1]
        # print(agent_mario_present_information_integer_x, 'x present information')
        agent_mario_present_information_integer_y = agent_mario_present_information_integer[1:2]
        # print(agent_mario_present_information_integer_y, 'y present information')

        agent_mario_past_memories_integer_x = agent_mario_past_memories_integer[0:1]
        # print(agent_mario_past_memories_integer_x, 'x memories information')
        agent_mario_past_memories_integer_y = agent_mario_past_memories_integer[1:2]
        # print(agent_mario_past_memories_integer_y, 'y memories information')

        """
        # separate future choice list for agent mario location comparison to present location
        agent_mario_future_choices_integer_x = agent_mario_future_choices_integer[0:1]
        agent_mario_future_choices_integer_y = agent_mario_future_choices_integer[1:2]
        agent_mario_future_choices_integer_action = agent_mario_future_choices_integer[2:3]

        agent_mario_future_choices_integer_x = agent_mario_future_choices_integer_x

        print(agent_mario_future_choices_integer_x, 'future choice x')
        print(agent_mario_future_choices_integer_y, 'future choice y')
        print(agent_mario_future_choices_integer_action, 'future choice action')
        """
        # compares x first then y but only x shows up on the print from *.append command trying a one time write
        # command to memories and then change the action and repeat until a positive result by current x is farther
        # ahead then past x and record that information of x y and action to future file to always perform same action
        # at same coordinates
        # standard run (number three) or walk action (number 8) for agent mario to perform instead of random choices
        # agent_mario_default_action_choice_list = [3, 3, 3, 8]
        # agent_mario_action = random.choice(agent_mario_default_action_choice_list)
        agent_mario_action = 8
        # add a new decision counter to test if agent mario is past point x where negative results happened
        # print(agent_mario_past_memories_integer, 'value memories second')
        # print(agent_mario_present_information_integer, 'value present second')
        # agent mario past memories location compare to present location to determine if new agent action is needed
        for i in agent_mario_past_memories_integer_x:
            # print(i, 'x for loop')
            if i in agent_mario_present_information_integer_x:
                for j in agent_mario_past_memories_integer_y:
                    # print(j, 'y for loop')
                    if j in agent_mario_present_information_integer_y:
                        while agent_mario_action == agent_mario_past_memories_integer[4]:
                            # agent_mario_action = np.random.random_integers(0, 4)
                            # print(agent_mario_action, 'new agent action')
                            agent_mario_action = 2
                            # decision counter activated test if agent mario is past x where negative results happened
                            with open('AgentMarioPastMemoriesCounter.txt', 'w', encoding='utf-8') as agent_mario_x_location_check_string:
                                agent_mario_x_location_check_string.write(str(1))
                                agent_mario_x_location_check_string.close()
                            with open('AgentMarioMemoriesAction.txt', 'w', encoding='utf-8') as agent_mario_memories_action_string:
                                agent_mario_memories_action_string.write(str(agent_mario_action))
                                agent_mario_memories_action_string.close()

        # check for new agent action activation and if activated start counter
        with open('AgentMarioPastMemoriesCounter.txt', 'r', encoding='utf-8') as agent_mario_x_location_check_string:
            agent_mario_x_location_check_integer = agent_mario_x_location_check_string
            agent_mario_x_location_check_integer = [eval(i) for i in agent_mario_x_location_check_integer]
            agent_mario_x_location_check_string.close()

        agent_mario_x_location_check_integer_counter = agent_mario_x_location_check_integer[0]

        # compare x location of agent mario to know if agent succeeded in action choice
        # check if counter is activated
        # changed from 5 to 12 as trying to find minimum distance needed to clear enemy without recording a
        # jump death into enemy as success
        if agent_mario_x_location_check_integer_counter >= 1 and agent_mario_x_location_check_integer_counter != 12:
            agent_mario_x_location_check_integer_counter += 1
            # print(agent_mario_x_location_check_integer_counter, '\n', '\n', '\n', '\n', 'counter')
            with open('AgentMarioPastMemoriesCounter.txt', 'w', encoding='utf-8') as agent_mario_x_location_counter_string:
                agent_mario_x_location_counter_string.write(str(agent_mario_x_location_check_integer_counter))
        # reset counter
        if agent_mario_x_location_check_integer_counter == 12:
            # check if agent x location past previous x past memories location
            # test = 'test'
            # print(test, '\n', '\n', '\n', '\n', 'test')
            # remove the integer from the list with the for statement for integer comparison
            # for i in agent_mario_past_memories_integer_x:
                # test = i
                # print(test, '\n', '\n', '\n', '\n', 'test')
            if agent_mario_present_information_integer_x > agent_mario_past_memories_integer_x:
                # add past memories x y locations and current agent action to future choices text file
                with open('AgentMarioMemoriesAction.txt', 'r', encoding='utf-8') as agent_mario_memories_action_string:
                    agent_mario_memories_action_integer = agent_mario_memories_action_string
                    agent_mario_memories_action_integer = [eval(i) for i in agent_mario_memories_action_integer]
                    agent_mario_memories_action_string.close()
                # create a list with agent marios information
                agents_marios_information_list = [agent_mario_past_memories_integer_x[0], agent_mario_past_memories_integer_y[0], agent_mario_memories_action_integer[0]]
                # print(agents_marios_information_list, '\n', '\n', '\n', '\n', 'test')
                # add successful agent mario information to future choices text file
                with open('AgentMarioFutureChoices.txt', 'a', encoding='utf-8') as future_choices_string:
                    future_choices_string.write(str(agents_marios_information_list))
                    future_choices_string.write('\n')
                    """
                    future_choices_string.write(str(agent_mario_past_memories_integer_x[0]))
                    future_choices_string.write('\n')
                    future_choices_string.write(str(agent_mario_past_memories_integer_y[0]))
                    future_choices_string.write('\n')
                    future_choices_string.write(str(agent_mario_memories_action_integer[0]))
                    """
                    future_choices_string.close()
                # reset counter
                with open('AgentMarioPastMemoriesCounter.txt', 'w', encoding='utf-8') as agent_mario_x_location_counter_string:
                    agent_mario_x_location_counter_string.write(str(0))
                    agent_mario_x_location_counter_string.close()
                # erase past memories text file
                # with open('AgentMarioPastMemories.txt', 'w', encoding='utf-8') as agent_mario_past_memories_string:
                    # agent_mario_past_memories_string.close()

        # print(agent_mario_x_location_check_integer_counter, '\n', '\n', '\n', '\n', 'counter test')

        # build future choices and present information lists for comparison
        agent_mario_present_comparison = agent_mario_present_information_integer[0:1]
        agent_mario_present_comparison_y = agent_mario_present_information_integer[1:2]
        agent_mario_present_comparison.extend(agent_mario_present_comparison_y)
        # print(agent_mario_present_comparison, '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', 'test present')

        # remove the nested list from the list
        agent_mario_future_comparison = agent_mario_future_choices_integer
        agent_mario_future_comparison = [i for j in agent_mario_future_comparison for i in j]

        # print(agent_mario_future_comparison, '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', 'test future')

        # loop iteration number to scan through whole future choice list until match or list finished
        while_loop_iteration_number = int(len(agent_mario_future_comparison) / 3)
        
        # create blank future comparison list and counter variables
        future_comparison_list = []
        i_iteration = 0
        j_iteration = 0
        agent_action_stored = 0
        
        # print(agent_mario_future_comparison, 'agent mario future comparison flattened list')

        # open files to determine if agent mario needs to continue high jump
        with open('HighJumpCounter.txt', 'r', encoding='utf-8') as high_jump_counter_string:
            high_jump_counter_integer_list = high_jump_counter_string
            high_jump_counter_integer_list = [eval(i) for i in high_jump_counter_integer_list]
            high_jump_counter_string.close()

        high_jump_counter_integer = high_jump_counter_integer_list[0]

        with open('HighJumpActivated.txt', 'r', encoding='utf-8') as high_jump_activated_string:
            high_jump_activated_integer = high_jump_activated_string
            high_jump_activated_integer = [eval(i) for i in high_jump_activated_integer]
            high_jump_activated_string.close()


        if high_jump_activated_integer == [0]:
            # create nested loop to create and compare future information lists with present information list
            while (i_iteration < while_loop_iteration_number) and (agent_mario_present_comparison != []):
                i_iteration += 1
                # compare lists
                if future_comparison_list == agent_mario_present_comparison:
                    agent_mario_action = agent_action_stored
                    # reset list for testing if works and break loop
                    future_comparison_list = []
                    # print('\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', 'works')
                    break
                else:
                    future_comparison_list = []
                while j_iteration < 3:
                    j_iteration += 1
                    # create future list to compare with present list
                    if j_iteration != 3:
                        future_comparison_list.append(agent_mario_future_comparison[0])
                        agent_mario_future_comparison.remove(agent_mario_future_comparison[0])
                        # print(future_comparison_list, 'temporary future compare list')
                        # print(agent_mario_future_comparison, 'flattened future list')
                    # reset counter and store agent action from list
                    if j_iteration == 3:
                        j_iteration = 0
                        agent_action_stored = agent_mario_future_comparison[0]
                        agent_mario_future_comparison.remove(agent_mario_future_comparison[0])
                        # print(agent_action_stored, 'agent action stored')
                        if future_comparison_list == agent_mario_present_comparison:
                            agent_mario_action = agent_action_stored
                            # reset list for testing if works and break loop
                            future_comparison_list = []
                            # store high jump (action key 4) to text file and start counter to ensure high jump
                            # reaches maximum height

                            with open('HighJumpActivated.txt', 'w', encoding='utf-8') as high_jump_activated_string:
                                high_jump_activated_string.write(str(1))
                                high_jump_activated_string.close()
                            with open('HighJumpCounter.txt', 'w', encoding='utf-8') as high_jump_counter_string:
                                high_jump_counter_string.write(str(1))
                                high_jump_counter_string.close()
                            # print(agent_mario_action, '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', 'works')
                        break
        else:
            agent_mario_random_choice = [4, 4]
            agent_mario_action = random.choice(agent_mario_random_choice)
            # agent_mario_action = 4
            high_jump_counter_integer += 1
            with open('HighJumpCounter.txt', 'w', encoding='utf-8') as high_jump_counter_string:
                high_jump_counter_string.write(str(high_jump_counter_integer))
                high_jump_counter_string.close()

            if high_jump_counter_integer == 40:
                with open('HighJumpCounter.txt', 'w', encoding='utf-8') as high_jump_counter_string:
                    high_jump_counter_string.write(str(0))
                    high_jump_counter_string.close()
                with open('HighJumpActivated.txt', 'w', encoding='utf-8') as high_jump_activated_string:
                    high_jump_activated_string.write(str(0))
                    high_jump_activated_string.close()
                agent_mario_action = 8

        # print(while_loop_iteration_number, 'number of lists in future choice text file')

        # check if agent mario needs to jump from being stuck is activated
        with open('AgentMarioIsStuckTimer.txt', 'r', encoding='utf-8') as agent_mario_activate_jump_string:
            agent_mario_activate_jump_integer = agent_mario_activate_jump_string
            agent_mario_activate_jump_integer = [eval(i) for i in agent_mario_activate_jump_integer]
            agent_mario_activate_jump_string.close()

        if agent_mario_activate_jump_integer == [1]:
            # if agent mario action key 4 then high jump is initiated and must continue for 25 i program cycles
            # one agent action i program cycle is not enough for agent to get full jump as agent needs several
            # i program cycles to complete a large jump before switching to another action then agent needs to
            # have activate jump file overwritten to allow activate jump test to happen again
            agent_mario_stuck_random_number_choice = [1, 4]
            agent_mario_action = random.choice(agent_mario_stuck_random_number_choice)
            # agent_mario_action = 4
            """
            # agent problem of getting stuck from enemy killing agent on left side and agent running into pipe at same time
            # does not occur because of timing not possible to check if course of action is a solution to problem changing
            # back to original code with different approach to problem
            agent_mario_action = 7
            with open('AgentMarioIsStuckTimer.txt', 'w', encoding='utf-8') as activate_jump:
                activate_jump.write(str(2))
                activate_jump.close()
        elif agent_mario_activate_jump_integer == [2]:
            agent_mario_action = 4
        # print(agent_mario_activate_jump_integer, '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', 'jump')
            """

        # check for if game over to press start action key and restart program to continue training
        with open('GameOver.txt', 'r', encoding='utf-8') as is_game_over_string:
            is_game_over_integer = is_game_over_string
            is_game_over_integer = [eval(i) for i in is_game_over_integer]
            is_game_over_string.close()

            # start button action key activate
            if is_game_over_integer == [255]:
                agent_mario_action = 5
                # print(agent_mario_action, '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', 'choice number')

        """
        # make luigi appear but he will not activate only sit idle as he does not respond to the action keys
        # and when timer runs out mario will activate and respond
        # accomplished on my grandfathers 95th birthday who killed mario to play luigi
        # 1/24/2023
        # start button action key activate
        if is_game_over_integer == [255]:
            # random_numbers_list = [5, 6]
            # agent_mario_action = random.choice(random_numbers_list)
            agent_mario_action = 6
            # print(agent_mario_action, '\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', 'choice number')
        elif (is_game_over_integer == [2]) and (agent_mario_action == 6):
            agent_mario_action = 5
        """

        # agent mario died in hole check
        """
        the super mario brother environment file, smb, cycles every other cycle and discrete cycles every cycle
        causing loss of information making agent mario exact information inaccurate 
        
        this causes crashes every now and then when information is needed from the present information text file or 
        other text files
        
        need a work around for jumping over certain holes and getting by death loops to enemys
        
        can try to make a present information file from check point to checkpoint using the holes as check points then
        appending to the file and using the appeneded present file instead of the curretn present file
        or in this case when a hole death occurs edit the information for the x coordinate to 
        be recorded to the file to get a coordinate that agent mario will collide with when the present information text
        file is called as to cause collision and match making agent mario commit to a new action
        
        can try writing several different x y coordinates to future file to get one of them to trigger to get 
        agent mario to jump 
        """
        with open('AgentMarioDiedInHole.txt', 'r', encoding='utf-8') as fall_death_string:
            fall_death_list = fall_death_string
            fall_death_list = [eval(i) for i in fall_death_list]
            fall_death_string.close()

        # agent mario died in hole counter
        with open('AgentMarioDiedInHoleCounter.txt', 'r', encoding='utf-8') as fall_death_counter_string:
            fall_death_counter_list = fall_death_counter_string
            fall_death_counter_list = [eval(i) for i in fall_death_counter_list]
            fall_death_counter_string.close()

        fall_death_integer = fall_death_list[0]
        fall_death_counter_integer = fall_death_counter_list[0]
        agent_mario_fall_death_avoid_square = 0

        # agent mario died in hole chose new agent action one to four squares previous
        # agent actions are 9 total greater then 9 equals agent mario died to hole change agent action before hole
        # when agent action is chosen use that action to max 40 program cycles before reset
        if (fall_death_integer > 0) and (fall_death_counter_integer == 0):

            # prepare agent action list choice before the hole
            agent_mario_fall_death_avoid = [fall_death_list[0] - 61,
                                            fall_death_list[0] - 45]

            # random agent choice location before the hole
            agent_mario_fall_death_avoid_square = np.random.choice(agent_mario_fall_death_avoid)

            # check when agent mario will perform new action
            if agent_mario_present_information_integer_x == agent_mario_fall_death_avoid_square:
                agent_mario_hole_random_number_choice = [1, 4]
                agent_mario_action = random.choice(agent_mario_hole_random_number_choice)
                #agent_mario_action = np.random.random_integers(0, 4)
                #agent_mario_action = 4
                # increment counter 30 times for maximum jump
                fall_death_counter_integer += 1
                with open('AgentMarioDiedInHoleCounter.txt', 'w', encoding='utf-8') as fall_death_counter_string:
                    fall_death_counter_string.write(str(fall_death_counter_integer))
                    fall_death_counter_string.close()
                with open('AgentMarioDiedInHole.txt', 'a', encoding='utf-8') as fall_death_counter_string:
                    fall_death_counter_string.write('\n')
                    fall_death_counter_string.write(str(agent_mario_fall_death_avoid_square))
                    fall_death_counter_string.write('\n')
                    fall_death_counter_string.write(str(4))
                    fall_death_counter_string.write('\n')
                    fall_death_counter_string.write(str(agent_mario_present_information_integer_y[0]))
                    fall_death_counter_string.close()

                # adding several workarounds for x y coordinates to get around the smb information cycle skip
                with open('AgentMarioFutureChoices.txt', 'a', encoding='utf-8') as future_write_string:
                    future_write_string.write(str([(fall_death_list[0] - 64),
                                                   agent_mario_present_information_integer_y[0],
                                                   4]))
                    future_write_string.write('\n')
                    future_write_string.write(str([(fall_death_list[0] - 44),
                                                   agent_mario_present_information_integer_y[0],
                                                   4]))
                    future_write_string.write('\n')
                    future_write_string.write(str([(fall_death_list[0] - 40),
                                                   agent_mario_present_information_integer_y[0],
                                                   4]))
                    future_write_string.write('\n')
                    future_write_string.write(str([(fall_death_list[0] - 34),
                                                   agent_mario_present_information_integer_y[0],
                                                   4]))
                    future_write_string.close()


        # complete agent mario action
        elif (fall_death_counter_integer >= 1) and (fall_death_counter_integer < 30):
            fall_death_counter_integer += 1
            with open('AgentMarioDiedInHoleCounter.txt', 'w', encoding='utf-8') as fall_death_counter_string:
                fall_death_counter_string.write(str(fall_death_counter_integer))
                fall_death_counter_string.close()
            with open('AgentMarioDiedInHole.txt', 'r', encoding='utf-8') as present_x_information_string:
                present_x_information_integer = present_x_information_string
                present_x_information_integer = [eval(i) for i in present_x_information_integer]
                present_x_information_string.close()
            # record information after counter hits maximum
            if fall_death_counter_integer == 30:
                with open('AgentMarioDiedInHole.txt', 'r', encoding='utf-8') as present_x_information_string:
                    present_x_information_integer = present_x_information_string
                    present_x_information_integer = [eval(i) for i in present_x_information_integer]
                    present_x_information_string.close()

                with open('AgentMarioDiedInHoleCounter.txt', 'w', encoding='utf-8') as fall_death_counter_string:
                    fall_death_counter_string.write(str(0))
                    fall_death_counter_string.close()

                # record success to future file and erase died in hole file
                # row zero is where agent mario died in hole
                # row one is the new agent mario square location choice
                # row two is new agent mario action
                # row three is y location of agent mario when square location choice was made
                with open('AgentMarioFutureChoices.txt', 'a', encoding='utf-8') as fall_death_string:
                    fall_death_string.write(str([present_x_information_integer[1],
                                                 present_x_information_integer[3],
                                                 present_x_information_integer[2]]))
                    fall_death_string.close()
                with open('AgentMarioDiedInHoleCounter.txt', 'w', encoding='utf-8') as fall_death_counter_string:
                    fall_death_counter_string.write(str(0))
                    fall_death_counter_string.close()

            agent_mario_hole_random_number = [1, 4]
            agent_mario_action = random.choice(agent_mario_hole_random_number)
            #agent_mario_action = 4

        print(agent_mario_action, 'agent mario action before return')
        return agent_mario_action

        # for RIGHT_ONLY action key movements
        # 0 = no movement, 1 = right movement walk (right), 2 = jump movement (right + A)
        # 3 = right movement run (right + B), 4 = jump right run movement (right + A + B)

        # agent mario performs a random action
        # agent_mario_action = np.random.random_integers(0, 4)
        # agent_mario_action = 2
        # return agent_mario_action
        # return np.random.random_integers(0, 4)
        # return statement selects a number from 0 to 4 to choose an action for agent mario from actions RIGHT_ONLY
        # return int(self.start + self.np_random.integers(self.n))

    def contains(self, x) -> bool:
        """Return boolean specifying if x is a valid member of this space."""
        if isinstance(x, int):
            as_int = x
        elif isinstance(x, (np.generic, np.ndarray)) and (
            np.issubdtype(x.dtype, np.integer) and x.shape == ()
        ):
            as_int = int(x)  # type: ignore
        else:
            return False

        return self.start <= as_int < self.start + self.n

    def __repr__(self) -> str:
        """Gives a string representation of this space."""
        if self.start != 0:
            return f"Discrete({self.n}, start={self.start})"
        return f"Discrete({self.n})"

    def __eq__(self, other) -> bool:
        """Check whether ``other`` is equivalent to this instance."""
        return (
            isinstance(other, Discrete)
            and self.n == other.n
            and self.start == other.start
        )

    def __setstate__(self, state):
        """Used when loading a pickled space.

        This method has to be implemented explicitly to allow for loading of legacy states.

        Args:
            state: The new state
        """
        # Don't mutate the original state
        state = dict(state)

        # Allow for loading of legacy states.
        # See https://github.com/openai/gym/pull/2470
        if "start" not in state:
            state["start"] = 0

        super().__setstate__(state)
