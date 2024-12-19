from bank import value

def test_not_h():
    assert value("fr") == 100
    assert value("") == 100
    assert value(" ") == 100
    assert value("  FR  ") == 100


def test_punctuation():
    assert value("123") == 100
    assert value("?hello") == 100


def test_h():
    assert value("hi") == 20
    assert value("Helo") == 20
    assert value("  heLo") == 20


def test_hello():
    assert value("Hello") == 0
    assert value("hello, world") == 0
    assert value("  hEllO, ") == 0