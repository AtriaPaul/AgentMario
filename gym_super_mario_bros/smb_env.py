"""An OpenAI Gym environment for Super Mario Bros. and Lost Levels."""
from collections import defaultdict

import gym.spaces.discrete
from nes_py import NESEnv
import numpy as np
from ._roms import decode_target
from ._roms import rom_path


# create a dictionary mapping value of status register to string names
_STATUS_MAP = defaultdict(lambda: 'fireball', {0:'small', 1: 'tall'})


# a set of state values indicating that Mario is "busy"
_BUSY_STATES = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x07]


# RAM addresses for enemy types on the screen
_ENEMY_TYPE_ADDRESSES = [0x0016, 0x0017, 0x0018, 0x0019, 0x001A]


# enemies whose context indicate that a stage change will occur (opposed to an
# enemy that implies a stage change wont occur -- i.e., a vine)
# Bowser = 0x2D
# Flagpole = 0x31
_STAGE_OVER_ENEMIES = np.array([0x2D, 0x31])


class SuperMarioBrosEnv(NESEnv):
    """An environment for playing Super Mario Bros with OpenAI Gym."""

    # the legal range of rewards for each step
    reward_range = (-15, 15)

    def __init__(self, rom_mode='vanilla', lost_levels=False, target=None):
        """
        Initialize a new Super Mario Bros environment.

        Args:
            rom_mode (str): the ROM mode to use when loading ROMs from disk
            lost_levels (bool): whether to load the ROM with lost levels.
                - False: load original Super Mario Bros.
                - True: load Super Mario Bros. Lost Levels
            target (tuple): a tuple of the (world, stage) to play as a level

        Returns:
            None

        """
        # decode the ROM path based on mode and lost levels flag
        rom = rom_path(lost_levels, rom_mode)
        # initialize the super object with the ROM path
        super(SuperMarioBrosEnv, self).__init__(rom)
        # set the target world, stage, and area variables
        target = decode_target(target, lost_levels)
        self._target_world, self._target_stage, self._target_area = target
        # setup a variable to keep track of the last frames time
        self._time_last = 0
        # setup a variable to keep track of the last frames x position
        self._x_position_last = 0
        # reset the emulator
        self.reset()
        # skip the start screen
        self._skip_start_screen()
        # create a backup state to restore from on subsequent calls to reset
        self._backup()

    @property
    def is_single_stage_env(self):
        """Return True if this environment is a stage environment."""
        return self._target_world is not None and self._target_area is not None

    # MARK: Memory access

    def _read_mem_range(self, address, length):
        """
        Read a range of bytes where each byte is a 10's place figure.

        Args:
            address (int): the address to read from as a 16 bit integer
            length: the number of sequential bytes to read

        Note:
            this method is specific to Mario where three GUI values are stored
            in independent memory slots to save processing time
            - score has 6 10's places
            - coins has 2 10's places
            - time has 3 10's places

        Returns:
            the integer value of this 10's place representation

        """
        return int(''.join(map(str, self.ram[address:address + length])))

    @property
    def _level(self):
        """Return the level of the game."""
        return self.ram[0x075f] * 4 + self.ram[0x075c]

    @property
    def _world(self):
        """Return the current world (1 to 8)."""
        return self.ram[0x075f] + 1

    @property
    def _stage(self):
        """Return the current stage (1 to 4)."""
        return self.ram[0x075c] + 1

    @property
    def _area(self):
        """Return the current area number (1 to 5)."""
        return self.ram[0x0760] + 1

    @property
    def _score(self):
        """Return the current player score (0 to 999990)."""
        # score is represented as a figure with 6 10's places
        return self._read_mem_range(0x07de, 6)

    @property
    def _time(self):
        """Return the time left (0 to 999)."""
        # time is represented as a figure with 3 10's places
        return self._read_mem_range(0x07f8, 3)

    @property
    def _coins(self):
        """Return the number of coins collected (0 to 99)."""
        # coins are represented as a figure with 2 10's places

        # print(self._read_mem_range(0x07ed, 2), 'coins number')

        return self._read_mem_range(0x07ed, 2)

    @property
    def _life(self):
        """Return the number of remaining lives."""
        # if commented out the game will go to game over screen and wait at start screen after three deaths
        # print(self.ram[0x075a], 'agent mario lives', '\n', '\n', '\n', '\n')
        return self.ram[0x075a]

    @property
    def _x_position(self):
        """Return the current horizontal position."""
        # add the current page 0x6d to the current x

        # agent_mario_x_position = np.uint8(int(self.ram[0x6d])) # * 0x100 + self.ram[0x86] - equals 0
        # agent_mario_x_position = self.ram[0x86] # - x position in integer form not ram address form
        # print(agent_mario_x_position)
        # agent_mario_x_position = self.ram[0x6d] * 0x100 + self.ram[0x86]
        # agent_mario_x_position = str(agent_mario_x_position)
        # print(self.ram[0x6d] * 0x100 + self.ram[0x86], 'agent mario x position in level')
        # print(self.ram[0x86], 'agent mario x position in level without current page added to mario position')
        # both formulas produce the same x position of agent mario
        # print(agent_mario_x_position)
        # return agent_mario_x_position

        # writes x location as
        # 1
        # 9
        # 1
        # with open('mario_x_location.txt', 'w', encoding='utf-8') as agent_mario_x_location_txt_file:
        #    agent_mario_x_location_txt_file.write('\n'.join(agent_mario_x_position))

        # writes x location as 191
        # with open('mario_x_location.txt', 'w', encoding='utf-8') as agent_mario_x_location_txt_file:
            # agent_mario_x_location_txt_file.write(agent_mario_x_position)

        return self.ram[0x6d] * 0x100 + self.ram[0x86]

    @property
    def _left_x_position(self):
        """Return the number of pixels from the left of the screen."""
        # TODO: resolve RuntimeWarning: overflow encountered in ubyte_scalars
        # subtract the left x position 0x071c from the current x 0x86
        # return (self.ram[0x86] - self.ram[0x071c]) % 256

        # this command does not execute

        return np.uint8(int(self.ram[0x86]) - int(self.ram[0x071c])) % 256

    @property
    def _y_pixel(self):
        """Return the current vertical position."""

        # print(self.ram[0x03b8], 'agent mario y pixel position')

        return self.ram[0x03b8]

    @property
    def _y_viewport(self):
        """
        Return the current y viewport.

        Note:
            1 = in visible viewport
            0 = above viewport
            > 1 below viewport (i.e. dead, falling down a hole)
            up to 5 indicates falling into a hole

        """
        # print(self.ram[0x00b5], 'viewport agent mario')
        return self.ram[0x00b5]

    @property
    def _y_position(self):
        """Return the current vertical position."""
        # check if Mario is above the viewport (the score board area)
        if self._y_viewport < 1:
            # y position overflows so we start from 255 and add the offset
            return 255 + (255 - self._y_pixel)
        # invert the y pixel into the distance from the bottom of the screen

        # print('smb_env file y position')
        # print(255 - self._y_pixel, 'agent mario y position')
        # print(self._y_pixel, 'viewport agent mario pixel')
        return 255 - self._y_pixel

    @property
    def _player_status(self):
        """Return the player status as a string."""
        return _STATUS_MAP[self.ram[0x0756]]

    @property
    def _player_state(self):
        """
        Return the current player state.

        Note:
            0x00 : Leftmost of screen
            0x01 : Climbing vine
            0x02 : Entering reversed-L pipe
            0x03 : Going down a pipe
            0x04 : Auto-walk
            0x05 : Auto-walk
            0x06 : Dead
            0x07 : Entering area
            0x08 : Normal
            0x09 : Cannot move
            0x0B : Dying
            0x0C : Palette cycling, can't move

        """
        # print(self.ram[0x000e])
        return self.ram[0x000e]

    @property
    def _is_dying(self):
        """Return True if Mario is in dying animation, False otherwise."""
        return self._player_state == 0x0b or self._y_viewport > 1

    @property
    def _is_dead(self):
        """Return True if Mario is dead, False otherwise."""
        # print(self._player_state == 0x06, 'life true/false')
        return self._player_state == 0x06

    @property
    def _is_game_over(self):
        """Return True if the game has ended, False otherwise."""
        # the life counter will get set to 255 (0xff) when there are no lives
        # left. It goes 2, 1, 0 for the 3 lives of the game
        return self._life == 0xff

    @property
    def _is_busy(self):
        """Return boolean whether Mario is busy with in-game garbage."""
        return self._player_state in _BUSY_STATES

    @property
    def _is_world_over(self):
        """Return a boolean determining if the world is over."""
        # 0x0770 contains GamePlay mode:
        # 0 => Demo
        # 1 => Standard
        # 2 => End of world
        return self.ram[0x0770] == 2

    @property
    def _is_stage_over(self):
        """Return a boolean determining if the level is over."""
        # iterate over the memory addresses that hold enemy types
        for address in _ENEMY_TYPE_ADDRESSES:
            # check if the byte is either Bowser (0x2D) or a flag (0x31)
            # this is to prevent returning true when Mario is using a vine
            # which will set the byte at 0x001D to 3
            if self.ram[address] in _STAGE_OVER_ENEMIES:
                # player float state set to 3 when sliding down flag pole
                return self.ram[0x001D] == 3

        return False

    @property
    def _flag_get(self):
        """Return a boolean determining if the agent reached a flag."""
        return self._is_world_over or self._is_stage_over

    # MARK: RAM Hacks

    def _write_stage(self):
        """Write the stage data to RAM to overwrite loading the next stage."""
        self.ram[0x075f] = self._target_world - 1
        self.ram[0x075c] = self._target_stage - 1
        self.ram[0x0760] = self._target_area - 1

    def _runout_prelevel_timer(self):
        """Force the pre-level timer to 0 to skip frames during a death."""
        self.ram[0x07A0] = 0

    def _skip_change_area(self):
        """Skip change area animations by by running down timers."""
        change_area_timer = self.ram[0x06DE]
        if change_area_timer > 1 and change_area_timer < 255:
            self.ram[0x06DE] = 1

    def _skip_occupied_states(self):
        """Skip occupied states by running out a timer and skipping frames."""
        while self._is_busy or self._is_world_over:
            self._runout_prelevel_timer()
            self._frame_advance(0)

    def _skip_start_screen(self):
        """Press and release start to skip the start screen."""
        # press and release the start button
        self._frame_advance(8)
        self._frame_advance(0)
        # Press start until the game starts
        while self._time == 0:
            # press and release the start button
            self._frame_advance(8)
            # if we're in the single stage, environment, write the stage data
            if self.is_single_stage_env:
                self._write_stage()
            self._frame_advance(0)
            # run-out the prelevel timer to skip the animation
            self._runout_prelevel_timer()
        # set the last time to now
        self._time_last = self._time
        # after the start screen idle to skip some extra frames
        while self._time >= self._time_last:
            self._time_last = self._time
            self._frame_advance(8)
            self._frame_advance(0)

    def _skip_end_of_world(self):
        """Skip the cutscene that plays at the end of a world."""
        if self._is_world_over:
            # get the current game time to reference
            time = self._time
            # loop until the time is different
            while self._time == time:
                # frame advance with NOP
                self._frame_advance(0)

    def _kill_mario(self):
        """Skip a death animation by forcing Mario to death."""
        # force Mario's state to dead
        self.ram[0x000e] = 0x06
        # step forward one frame
        self._frame_advance(0)

    # MARK: Reward Function

    @property
    def _x_reward(self):
        """Return the reward based on left right movement between steps."""
        _reward = self._x_position - self._x_position_last
        self._x_position_last = self._x_position
        # TODO: check whether this is still necessary
        # resolve an issue where after death the x position resets. The x delta
        # is typically has at most magnitude of 3, 5 is a safe bound
        if _reward < -5 or _reward > 5:
            return 0

        return _reward

    @property
    def _time_penalty(self):
        """Return the reward for the in-game clock ticking."""
        _reward = self._time - self._time_last
        self._time_last = self._time
        # time can only decrease, a positive reward results from a reset and
        # should default to 0 reward
        if _reward > 0:
            return 0

        return _reward

    @property
    def _death_penalty(self):
        """Return the reward earned by dying."""
        if self._is_dying or self._is_dead:
            return -25

        return 0

    # MARK: nes-py API calls

    def _will_reset(self):
        """Handle and RAM hacking before a reset occurs."""
        self._time_last = 0
        self._x_position_last = 0

    def _did_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        self._time_last = self._time
        self._x_position_last = self._x_position

    def _did_step(self, done):
        """
        Handle any RAM hacking after a step occurs.

        Args:
            done: whether the done flag is set to true

        Returns:
            None

        """
        # if done flag is set a reset is incoming anyway, ignore any hacking
        if done:
            return
        # if mario is dying, then cut to the chase and kill hi,
        if self._is_dying:
            self._kill_mario()
        # skip world change scenes (must call before other skip methods)
        if not self.is_single_stage_env:
            self._skip_end_of_world()
        # skip area change (i.e. enter pipe, flag get, etc.)
        self._skip_change_area()
        # skip occupied states like the black screen between lives that shows
        # how many lives the player has left
        self._skip_occupied_states()

    def _get_reward(self):
        """Return the reward after a step occurs."""
        return self._x_reward + self._time_penalty + self._death_penalty

    def _get_done(self):
        """Return True if the episode is over, False otherwise."""
        if self.is_single_stage_env:
            return self._is_dying or self._is_dead or self._flag_get
        return self._is_game_over

    def _get_info(self):
        """Return the info after a step occurs"""

        # writes a file that is still being used but is not a text file
        # with open('information_test', 'w', encoding='utf-8') as information_test:
        #    information_test.write(str(dict(
        #                                    x_position=self._x_position,
        #                                    y_position=self._y_position,
        #                                    )))
        # using a dictionary for string as list
        """
        with open('information_test_dictionary.txt', 'w', encoding='utf-8') as information_test_dictionary:
            information_test_dictionary.write(str(dict(
                                            x_position=self._x_position,
                                            y_position=self._y_position,
                                            )))
        """

        """
        with open('information_test_list.txt', 'w', encoding='utf-8') as information_test_list:
            information_test_list.write(str(
                [self._x_position, self._y_position]
            ))
        """

        # store the present information about agent mario
        # row zero x location
        # row one y location
        # row two agent mario dead 11 or alive 8
        # row three in game world timer
        # row four agent marios current action
        # print('environment information record')
        with open('AgentMarioPresentInformation.txt', 'w', encoding='utf-8') as agent_mario_present_information_string:
            agent_mario_present_information_string.write(str(self._x_position))
            agent_mario_present_information_string.write('\n')
            agent_mario_present_information_string.write(str(self._y_position))
            agent_mario_present_information_string.write('\n')
            agent_mario_present_information_string.write(str(self._player_state))
            agent_mario_present_information_string.write('\n')
            agent_mario_present_information_string.write(str(self._read_mem_range(0x07f8, 3)))
            agent_mario_present_information_string.write('\n')
            agent_mario_present_information_string.write(str(gym.spaces.discrete.Discrete.sample(self)))
            # print('smb file', str(gym.spaces.discrete.Discrete.sample(self)))

            # close text file to allow continues reading/writing to file
            agent_mario_present_information_string.close()

        # print(str(gym.spaces.discrete.Discrete.sample(self)))

        # store the past memories of agent mario if agent mario dies
        # the stored information in the text file is delayed and still shows agent alive status 8
        # the program stops recording information once agent dies and equals agent status 11 and does not record
        # the information for current agent status
        if self._player_state == 11:
            # print('agent died')
            # write the list file in multiple rows
            with open('AgentMarioPastInformation.txt', 'r', encoding='utf-8') as agent_mario_past_information_string:
                agent_mario_past_memories_string = agent_mario_past_information_string
                agent_mario_past_memories_integer = [eval(i) for i in agent_mario_past_memories_string]
            with open('AgentMarioPastMemories.txt', 'w', encoding='utf-8') as agent_mario_past_memories_string_temp:
                agent_mario_past_memories_string_temp.write(str(agent_mario_past_memories_integer[0] - 2))
                agent_mario_past_memories_string_temp.write('\n')
                agent_mario_past_memories_string_temp.write(str(agent_mario_past_memories_integer[1]))
                agent_mario_past_memories_string_temp.write('\n')
                agent_mario_past_memories_string_temp.write(str(agent_mario_past_memories_integer[2]))
                agent_mario_past_memories_string_temp.write('\n')
                agent_mario_past_memories_string_temp.write(str(agent_mario_past_memories_integer[3]))
                agent_mario_past_memories_string_temp.write('\n')
                agent_mario_past_memories_string_temp.write(str(agent_mario_past_memories_integer[4]))
                agent_mario_past_memories_string_temp.write('\n')
                agent_mario_past_memories_string_temp.close()
                """
                # write in list format
                agent_mario_past_memories_string_temp.write(str(agent_mario_past_memories_integer))
                agent_mario_past_memories_string_temp.write('\n')
                agent_mario_past_memories_string_temp.write(str(agent_mario_past_memories_integer))
                agent_mario_past_memories_string_temp.write('\n')
                agent_mario_past_memories_string_temp.write(str(agent_mario_past_memories_integer))
                agent_mario_past_memories_string_temp.write('\n')
                agent_mario_past_memories_string_temp.write(str(agent_mario_past_memories_integer))
                agent_mario_past_memories_string_temp.write('\n')
                agent_mario_past_memories_string_temp.write(str(agent_mario_past_memories_integer))
                agent_mario_past_memories_string_temp.close()
                """
                # close text file to allow continues reading/writing to file
                agent_mario_past_information_string.close()

            # create a trailing memories file to prevent agent mario from getting stuck in fall/jump death to an enemy
            trailing_memories_build_list = []

            with open('AgentMarioTrailingPastMemories.txt', 'r', encoding='utf-8') as trailing_memories_string:
                trailing_memories_integer_list = trailing_memories_string
                trailing_memories_integer_list = [eval(i) for i in trailing_memories_integer_list]
                trailing_memories_string.close()

            # flatten list
            trailing_memories_integer_list = [i for j in trailing_memories_integer_list for i in j]
            # print(trailing_memories_integer_list)
            # record death coordinates and start death counter to determine if stuck in death loop to enemy
            if trailing_memories_integer_list[0] == 0:
                # death counter
                trailing_memories_integer_list[0] += 1
                # death x y coordinates
                trailing_memories_integer_list[1] = self._x_position
                trailing_memories_integer_list[2] = self._y_position

                # build x y agent action list for trailing memories text file
                trailing_memories_build_list = [trailing_memories_integer_list[1], trailing_memories_integer_list[2],
                                                trailing_memories_integer_list[3]]
                """
                # build list for trailing memories text file
                trailing_memories_build_list = [trailing_memories_integer_list[0],
                                                [trailing_memories_integer_list[1], trailing_memories_integer_list[2],
                                                trailing_memories_integer_list[3]]]
                records as [1, [296, 79, 1]] and this will not work with list code design
                """
                # print(trailing_memories_build_list, '\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n',)
                with open('AgentMarioTrailingPastMemories.txt', 'w', encoding='utf-8') as record_death_location_string:
                    record_death_location_string.write(str([trailing_memories_integer_list[0]]))
                    record_death_location_string.write('\n')
                    record_death_location_string.write(str(trailing_memories_build_list))
                    record_death_location_string.close()

            # test if agent mario is stuck in death loop at same location to same enemy
            elif (trailing_memories_integer_list[0] < 2) and ((trailing_memories_integer_list[1] == self._x_position) and (trailing_memories_integer_list[2] == self._y_position)):
                trailing_memories_integer_list[0] += 1
                # print('working')
                # build list for trailing memories text file
                trailing_memories_build_list = [trailing_memories_integer_list[1],
                                                trailing_memories_integer_list[2],
                                                trailing_memories_integer_list[3]]

                # print(trailing_memories_build_list, '\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n',)
                with open('AgentMarioTrailingPastMemories.txt', 'w', encoding='utf-8') as record_death_location_string:
                    record_death_location_string.write(str([trailing_memories_integer_list[0]]))
                    record_death_location_string.write('\n')
                    record_death_location_string.write(str(trailing_memories_build_list))
                    record_death_location_string.close()

            # agent mario is stuck in death loop end loop
            elif trailing_memories_integer_list[0] == 2:
                trailing_memories_integer_choice = [trailing_memories_integer_list[1] - 31,
                                                    trailing_memories_integer_list[1] - 67,
                                                    ]
                trailing_memories_integer_choice_selected = np.random.choice(trailing_memories_integer_choice)
                agent_mario_death_loop_end = [trailing_memories_integer_choice_selected, trailing_memories_integer_list[2],
                                              np.random.random_integers(0, 4)]

                """
                            trailing_memories_integer_list[1] -= 64
                            agent_mario_death_loop_end = [trailing_memories_integer_list[1], trailing_memories_integer_list[2],
                                                              np.random.random_integers(0, 4)]
                """

                # add to future file to end death loop four squares back from previous location
                with open('AgentMarioFutureChoices.txt', 'a', encoding='utf-8') as agent_mario_death_loop_end_string:
                    agent_mario_death_loop_end_string.write(str(agent_mario_death_loop_end))
                    agent_mario_death_loop_end_string.write('\n')
                    agent_mario_death_loop_end_string.close()
                # reset death loop file
                with open('AgentMarioTrailingPastMemories.txt', 'w', encoding='utf-8') as record_death_location_string:
                    record_death_location_string.write(str([0]))
                    record_death_location_string.write('\n')
                    record_death_location_string.write(str([1, 1, 1]))
                    record_death_location_string.close()
            # agent mario died in a new location and death counter and location need updating
            elif (trailing_memories_integer_list[0] >= 1) and (trailing_memories_integer_list[1] != self._x_position) and (trailing_memories_integer_list[1] != 1):
                # death counter
                trailing_memories_integer_list[0] = 1
                # death x y coordinates
                trailing_memories_integer_list[1] = self._x_position
                trailing_memories_integer_list[2] = self._y_position

                # build x y agent action list for trailing memories text file
                trailing_memories_build_list = [trailing_memories_integer_list[1], trailing_memories_integer_list[2],
                                                trailing_memories_integer_list[3]]
                # print(trailing_memories_build_list, '\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n',)
                with open('AgentMarioTrailingPastMemories.txt', 'w', encoding='utf-8') as record_death_location_string:
                    record_death_location_string.write(str([trailing_memories_integer_list[0]]))
                    record_death_location_string.write('\n')
                    record_death_location_string.write(str(trailing_memories_build_list))
                    record_death_location_string.close()

            """     
            # increment the counter in the list until 4 to know is agent mario is stuck in same location or not
            # add x y coordinates to test with present coordinates
            if (trailing_memories_integer_list[0] > 0) and (trailing_memories_integer_list[0] < 4):
                trailing_memories_integer_list[0] += 1
                print('working', '\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n','\n')
            # build trailing memories list back to text file
            # erase file to prepare to build list back to file
            with open('AgentMarioTrailingPastMemories.txt', 'w', encoding='utf-8') as erase_text_file:
                erase_text_file.write(str([0]))
                erase_text_file.write('\n')
                erase_text_file.close()

            # write the trailing memories back to text file
            while i_iteration <= 3:
                i_iteration += 1
                if i_iteration <= 3:
                    future_choice_build_list.append(future_choice_duplicates_removed[0])
                    future_choice_duplicates_removed.remove(future_choice_duplicates_removed[0])
                if i_iteration == 4:
                    i_iteration = 0
                    with open('AgentMarioTrailingPastMemories.txt', 'a', encoding='utf-8') as trailing_memories_string:
                        duplicates_removed_test_string.write(str(future_choice_build_list))
                        duplicates_removed_test_string.write('\n')
                        trailing_memories_string.close()
                    trailing_memories_build_list = []
                    break
            """


        # record agent mario lives to text file to know when to activate start button action key to restart program
        if self._life == 255:
            with open('GameOver.txt', 'w', encoding='utf-8') as game_over_string:
                game_over_string.write(str(self._life))
                game_over_string.close()
        elif self._life == 2:
            with open('GameOver.txt', 'w', encoding='utf-8') as game_over_string:
                game_over_string.write(str(self._life))
                game_over_string.close()
            # print('\n', '\n', '\n', '\n', '\n', '\n', '\n', '\n', 'game over')

        # agent mario fall death into a hole data record
        if self._y_viewport >= 2:
            with open('AgentMarioDiedInHole.txt', 'w', encoding='utf-8') as fall_death_string:
                fall_death_string.write(str(self._x_position))
                fall_death_string.close()

        return dict(
            coins=self._coins,
            flag_get=self._flag_get,
            life=self._life,
            score=self._score,
            stage=self._stage,
            status=self._player_status,
            time=self._time,
            world=self._world,
            x_pos=self._x_position,
            y_pos=self._y_position,
        )


# explicitly define the outward facing API of this module
__all__ = [SuperMarioBrosEnv.__name__]
