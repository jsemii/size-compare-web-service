from app.services.compare import convert_unit

def test_convert_unit_cm():
    assert convert_unit(100.0, "cm") == 100.0

def test_convert_unit_inch():
    assert convert_unit(2.54, "inch") == 1.0

def test_convert_unit_none():
    assert convert_unit(None, "cm") is None

def test_convert_unit_round():
    assert convert_unit(10.0, "inch") == 3.9