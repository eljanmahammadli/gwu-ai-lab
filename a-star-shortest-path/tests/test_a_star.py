from shortestpath.main import txt_parser, a_star

def test_a_star_case_1():
    filename = "inputs/input1.txt"
    pitcher_capacities, start_volumes, target_volume = txt_parser(filename)
    res, result_state, visited = a_star(start_volumes, pitcher_capacities, target_volume)
    assert res == 7

def test_a_star_case_2():
    filename = "inputs/input2.txt"
    pitcher_capacities, start_volumes, target_volume = txt_parser(filename)
    res, result_state, visited = a_star(start_volumes, pitcher_capacities, target_volume)
    assert res == -1

def test_a_star_case_3():
    filename = "inputs/input3.txt"
    pitcher_capacities, start_volumes, target_volume = txt_parser(filename)
    res, result_state, visited = a_star(start_volumes, pitcher_capacities, target_volume)
    assert res == -1

def test_a_star_case_4():
    filename = "inputs/input4.txt"
    pitcher_capacities, start_volumes, target_volume = txt_parser(filename)
    res, result_state, visited = a_star(start_volumes, pitcher_capacities, target_volume)
    assert res == 37

def test_a_star_case_5():
    filename = "inputs/input5.txt"
    pitcher_capacities, start_volumes, target_volume = txt_parser(filename)
    res, result_state, visited = a_star(start_volumes, pitcher_capacities, target_volume)
    assert res == 20

    