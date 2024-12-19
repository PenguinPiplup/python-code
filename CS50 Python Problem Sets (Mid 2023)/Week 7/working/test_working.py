from working import convert
import pytest

def test_convert_1():
    assert convert("9:00 AM to 5:00 PM") == "09:00 to 17:00"
    assert convert("09:00 AM to 04:30 PM") == "09:00 to 16:30"
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"

def test_convert_2():
    assert convert("9 AM to 5:30 PM") == "09:00 to 17:30"
    assert convert("5 PM to 11 AM") == "17:00 to 11:00"
    assert convert("12:00 AM to 12:00 PM") == "00:00 to 12:00"

def test_convert_invalid():
    with pytest.raises(ValueError):
        convert("9:60 AM to 5:00 PM")
    with pytest.raises(ValueError):
        convert("9:00 AM - 5:00 PM")
    with pytest.raises(ValueError):
        convert("13:00 AM to 9:00 AM")
    with pytest.raises(ValueError):
        convert("12:00 AM to 13:00 PM")
    with pytest.raises(ValueError):
        convert("12:00 to 10:00")