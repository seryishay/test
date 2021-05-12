import math_func
import pytest


class TestClass:
    def test_add(self):
        assert math_func.add(1,2) == 3

    def test_add_2(self):
        assert math_func.add(1,4) == 3
