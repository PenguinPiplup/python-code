from plates import is_valid

def test_alpha():
    assert is_valid("AA") == True
    # assert is_valid(" AA") == True
    # assert is_valid(" A") == False
    assert is_valid("A") == False
    assert is_valid("ABCDEFG") == False
    assert is_valid("ABCDE") == True
    # assert is_valid("ABCDE  ") == True
    # assert is_valid("aab") == True


def test_symbols():
    assert is_valid("AA%!") == False
    assert is_valid("AAB/") == False
    assert is_valid("%^&%") == False


def test_zero():
    assert is_valid("AA01") == False
    assert is_valid("AA101") == True
    assert is_valid("AAB0") == False
    assert is_valid("AA0") == False
    assert is_valid("AA10") == True


def test_numbers():
    assert is_valid("AA3345") == True
    assert is_valid("AA45654") == False
    assert is_valid("A2019") == False
    assert is_valid("404") == False
    assert is_valid("AA43R") == False