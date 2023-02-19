"""Static action sets for binary to discrete action space wrappers."""


# actions for the simple run right environment

RIGHT_ONLY = [
    ['NOOP'],
    ['right'],
    ['right', 'A'],
    ['right', 'B'],
    ['right', 'A', 'B'],
]

# jump right actions with a run to get longer higher jumps

JUMP_RIGHT_ONLY = [
    ['right', 'A', 'B'],
    ['right', 'A'],
    ['right', 'B'],
    ['right', 'A', 'B'],
    ['right', 'B', 'A'],
    ['start'],
    ['select'],
    ['left'],
    ['right'],
]


# actions for very simple movement
SIMPLE_MOVEMENT = [
    ['NOOP'],
    ['right'],
    ['right', 'A'],
    ['right', 'B'],
    ['right', 'A', 'B'],
    ['A'],
    ['left'],
]


# actions for more complex movement
COMPLEX_MOVEMENT = [
    ['NOOP'],
    ['right'],
    ['right', 'A'],
    ['right', 'B'],
    ['right', 'A', 'B'],
    ['A'],
    ['left'],
    ['left', 'A'],
    ['left', 'B'],
    ['left', 'A', 'B'],
    ['down'],
    ['up'],
]
