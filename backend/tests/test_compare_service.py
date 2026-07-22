from app.services.compare import convert_unit
from app.services.compare import convert_unit, build_message

def test_convert_unit_cm():
    assert convert_unit(100.0, "cm") == 100.0

def test_convert_unit_inch():
    assert convert_unit(2.54, "inch") == 1.0

def test_convert_unit_none():
    assert convert_unit(None, "cm") is None

def test_convert_unit_round():
    assert convert_unit(10.0, "inch") == 3.9

def test_build_message_positive():
    assert build_message(2.0, "cm") == "내 옷보다 +2.0cm 큽니다"

def test_build_message_negative():
    assert build_message(-1.0, "cm") == "내 옷보다 -1.0cm 작습니다"

def test_build_message_zero():
    assert build_message(0.0, "cm") == "내 옷과 같습니다"