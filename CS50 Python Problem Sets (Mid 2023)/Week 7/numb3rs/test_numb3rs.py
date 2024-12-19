from numb3rs import validate

def test_length():
    assert validate("234.123.133.32") == True
    assert validate("234.123.133") == False
    assert validate("234.123.133.32.32") == False


def test_255():
    assert validate("255.255.0.0") == True
    assert validate("0.0.0.256") == False
    assert validate("255.255.255.-1") == False


def test_not_number():
    assert validate("ree.lkd.loj.hrk") == False
    assert validate(":ef.sae.kwk.$ed") == False
    assert validate(":45.54.23.43") == False