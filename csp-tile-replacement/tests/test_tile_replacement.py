
from tileplacement.main import load_landscape, TilePlacementProblem

def test_select_unassigned_var():
    filename = "problems/tilesproblem_01.txt"
    landscape, constraints = load_landscape(filename)
    tpp = TilePlacementProblem(landscape, constraints)
    tpp.bushes[0].tile = 'FULL_BLOCK'
    tpp.bushes[1].tile = 'FULL_BLOCK'
    var = tpp.select_unassigned_var()
    assert var == 2


def test_is_complete_1():
    filename = "problems/tilesproblem_01.txt"
    landscape, constraints = load_landscape(filename)
    tpp = TilePlacementProblem(landscape, constraints)
    tpp.bushes[0].tile = 'FULL_BLOCK'
    tpp.bushes[1].tile = 'FULL_BLOCK'
    result = tpp.is_complete()
    assert result == False

def test_is_complete_2():
    filename = "problems/tilesproblem_01.txt"
    landscape, constraints = load_landscape(filename)
    tpp = TilePlacementProblem(landscape, constraints)
    for i in range(25):
        tpp.bushes[i].tile = 'FULL_BLOCK'
    result = tpp.is_complete()
    assert result == None


def test_inconsistent_bush_counts():
    filename = "problems/tilesproblem_01.txt"
    landscape, constraints = load_landscape(filename)
    tpp = TilePlacementProblem(landscape, constraints)
    for i in range(24):
        tpp.bushes[i].tile = 'FULL_BLOCK'
    result = tpp.is_consistent(24, 'FULL_BLOCK')
    assert result == True
