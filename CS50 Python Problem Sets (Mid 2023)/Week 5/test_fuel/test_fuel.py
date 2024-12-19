from fuel import convert
from fuel import gauge
import pytest

def test_convert():
    assert convert("0/100") == 0
    assert convert("3/4") == 75
    assert convert("4/5") == 80
    assert convert("99/99") == 100


def test_convert_invalid():
    with pytest.raises(ValueError):
        convert("cat/dog")
    with pytest.raises(ValueError):
        convert("fg/3")
    with pytest.raises(ValueError):
        convert("5/3")
    with pytest.raises(ZeroDivisionError):
        convert("5/0")


def test_gauge():
    assert gauge(0) == "E"
    assert gauge(1) == "E"
    assert gauge(34) == "34%"
    assert gauge(50) == "50%"
    assert gauge(99) == "F"
    assert gauge(100) == "F"