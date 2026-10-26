import pytest

from src.pell.solver import pells_solver, find_largest_minimal_x


def test_pell_solution_d2():
    assert pells_solver(2) == (3, 2)


def test_pell_solution_d3():
    assert pells_solver(3) == (2, 1)


def test_pell_solution_d5():
    assert pells_solver(5) == (9, 4)


def test_pell_solution_d13():
    assert pells_solver(13) == (649, 180)


def test_pell_solution_d61():
    assert pells_solver(61) == (1766319049, 226153980)

def test_pell_equation_is_satisfied():
    for D in [2, 3, 5, 13, 61, 94, 9949]:
        x, y = pells_solver(D)

        assert x * x - D * y * y == 1
        assert x > 0
        assert y > 0

def test_find_largest_minimal_x():
    best_D, max_x, best_y = find_largest_minimal_x(10000)

    assert best_D == 9949
    assert max_x == 23551019614858223475933893515741198183163217312913587552899320396564478041197360918469501097146448985821854465768234479384482435117587576296319428592757548743265811454938493105633433315887574461850060798834186249
    assert max_x * max_x - best_D * best_y * best_y == 1

def test_pells_solver_value_error():
    pytest.raises(ValueError, lambda: pells_solver(4))

@pytest.mark.parametrize("D", [-1, 0, 1])
def test_pells_solver_rejects_values_below_2(D):
    with pytest.raises(ValueError):
        pells_solver(D)

@pytest.mark.parametrize("D", [2.5, 3.0, True])
def test_pells_solver_rejects_non_integer_inputs(D):
    with pytest.raises(TypeError):
        pells_solver(D)


@pytest.mark.parametrize("D", [-1, 0, 1])
def test_find_largest_minimal_x_rejects_values_below_2(D):
    with pytest.raises(ValueError):
        find_largest_minimal_x(D)

@pytest.mark.parametrize("D", [2.5, 3.0, True])
def test_find_largest_minimal_x_rejects_non_integer_inputs(D):
    with pytest.raises(TypeError):
        find_largest_minimal_x(D)