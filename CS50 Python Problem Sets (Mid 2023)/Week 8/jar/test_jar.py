from jar import Jar
import pytest

def test_init():
    jar = Jar(12)
    assert jar.capacity == 12

def test_str():
    jar = Jar()
    jar.deposit(5)
    assert str(jar) == "🍪🍪🍪🍪🍪"

def test_deposit():
    jar = Jar(12)
    jar.deposit(5)
    assert jar.size == 5
    jar.deposit(6)
    assert jar.size == 11
    with pytest.raises(ValueError):
        jar.deposit(2)

def test_withdraw():
    jar = Jar()
    jar.deposit(4)
    jar.withdraw(2)
    assert jar.size == 2
    jar.withdraw(2)
    assert jar.size == 0
    with pytest.raises(ValueError):
        jar.withdraw(3)