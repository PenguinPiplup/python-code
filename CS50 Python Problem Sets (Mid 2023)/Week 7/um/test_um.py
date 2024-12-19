from um import count

def test_upperlower():
    assert count("Um...") == 1
    assert count("uM") == 1
    assert count("g um") == 1

def test_whitespace():
    assert count(" um,thanks for helping") == 1
    assert count("yes,um") == 1

def test_not_um():
    assert count("Um, thanks for the album.") == 1
    assert count(".um. sum ?um bum") == 2
    assert count("yummy yum") == 0

def test_multiple_um():
    #assert count("um um um umu um ") == 4
    #assert count("um UM! yumyum mu ...um helium") == 3
    # Deprecation warning
    assert count("um, today i am here to um... share um... what was i gonna um... say?") == 4