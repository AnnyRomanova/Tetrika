import pytest
from solution import sum_two

def test_strict_correct():
    assert sum_two(1, 2) == 3

def test_strict_wrong():
    with pytest.raises(TypeError):
        sum_two(1, 2.4)