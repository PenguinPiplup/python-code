from twttr import shorten

def test_shorten_upper():
    assert shorten("ABCEIOU") == "BC"


def test_shorten_lower():
    assert shorten("abceiou") == "bc"


def test_shorten_others():
    assert shorten("./,1230test") == "./,1230tst"