import pytest

def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mul(a,b):
    return a*b
def div(a,b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a/b
    
def test_add():
    assert add(2,3) == 5
    assert add(-1,1) == 0
    assert add(0,0) == 0

# def test_fail():
#     assert add(2,2) == 5

def test_sub():
    assert sub(5,3) == 2
    assert sub(0,1) == -1
    assert sub(-1,-1) == 0
def test_mul():
    assert mul(2,3) == 6
    assert mul(-1,1) == -1
    assert mul(0,5) == 0

def test_div():
    assert div(6,3) == 2
    assert div(-4,2) == -2
    with pytest.raises(ValueError):
        div(5,0)



