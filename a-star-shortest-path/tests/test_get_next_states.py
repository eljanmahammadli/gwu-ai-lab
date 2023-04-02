import numpy as np
# from shortest_path 
from shortestpath.main import get_next_states, State

def test_get_next_states_case_1():
    capacities = [np.inf, 2, 5, 6, 72]
    state = State([0, 0, 0, 0, 0])
    next_states = get_next_states(state, capacities)
    excepted = [
        State([0, 2, 0, 0, 0]),
        State([0, 0, 5, 0, 0]),
        State([0, 0, 0, 6, 0]),
        State([0, 0, 0, 0, 72])
    ]
    assert next_states == excepted


def test_get_next_states_case_2():
    capacities = [np.inf, 2, 5, 6, 72]
    state = State([0, 0, 0, 0, 72])
    next_states = get_next_states(state, capacities)
    excepted = [
        State([72, 0, 0, 0, 0]),
        State([0, 2, 0, 0, 70]),
        State([0, 0, 5, 0, 67]),
        State([0, 0, 0, 6, 66]),
        State([0, 2, 0, 0, 72]),
        State([0, 0, 5, 0, 72]),
        State([0, 0, 0, 6, 72])
    ]
    assert next_states == excepted


def test_get_next_states_case_3():
    capacities = [np.inf, 3, 5]
    state = State([3, 3, 0])
    next_states = get_next_states(state, capacities)
    excepted = [
        State([0, 3, 3]),
        State([6, 0, 0]),
        State([3, 0, 3]),
        State([3, 3, 5])
    ]
    assert next_states == excepted