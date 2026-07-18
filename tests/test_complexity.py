# tests/test_complexity.py
from src.compute_complexity import compute_code_complexity
def test_simple_complexity():

    code = """
def hello():
    return 1

"""
    result = compute_code_complexity(code)
    assert result is not None
    assert result["max"] == 1

def test_if_statement_complexity():
    code = """
def check(x):
    if x:
        return True
    return False

"""
    result = compute_code_complexity(code)
    assert result["max"] == 2