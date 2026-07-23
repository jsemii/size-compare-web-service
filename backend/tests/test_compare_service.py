from app.services.compare import convert_unit, build_message, compare_garment_with_wish
from types import SimpleNamespace

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


def test_compare_all_fields_filled():
    garment = SimpleNamespace(
        name="내 티셔츠",
        total_length_cm=70.0,
        shoulder_cm=45.0,
        chest_cm=52.0,
        sleeve_cm=20.0,
        waist_cm=50.0,
        hip_cm=54.0
    )
    wish = SimpleNamespace(
        name="위시 티셔츠",
        total_length_cm=72.0,
        shoulder_cm=47.0,
        chest_cm=54.0,
        sleeve_cm=22.0,
        waist_cm=52.0,
        hip_cm=56.0
    )

    result = compare_garment_with_wish(garment, wish, "cm")

    assert result.compared_count == 6
    assert result.missing_count == 0
    assert result.unit == "cm"
    assert len(result.items) == 6
    assert result.items[0].field == "total_length"
    assert result.items[0].diff == 2.0



def test_compare_missing_field():
    garment = SimpleNamespace(
        name="내 티셔츠",
        total_length_cm=70.0,
        shoulder_cm=45.0,
        chest_cm=52.0,
        sleeve_cm=20.0,
        waist_cm=50.0,
        hip_cm=None
    )
    wish = SimpleNamespace(
        name="위시 티셔츠",
        total_length_cm=72.0,
        shoulder_cm=47.0,
        chest_cm=54.0,
        sleeve_cm=22.0,
        waist_cm=52.0,
        hip_cm=56.0
    )

    result = compare_garment_with_wish(garment, wish, "cm")

    assert result.compared_count == 5
    assert result.missing_count == 1
    assert result.unit == "cm"
    assert len(result.items) == 6
    assert result.items[5].comparable is False
    assert result.items[5].diff is None
    assert result.items[0].comparable is True
    assert result.items[5].wish_cloth is None



def test_compare_inch_unit():
    garment = SimpleNamespace(
        name="내 티셔츠",
        total_length_cm=25.4,
        shoulder_cm=25.4,
        chest_cm=25.4,
        sleeve_cm=25.4,
        waist_cm=25.4,
        hip_cm=25.4
    )
    wish = SimpleNamespace(
        name="위시 티셔츠",
        total_length_cm=27.94,
        shoulder_cm=27.94,
        chest_cm=27.94,
        sleeve_cm=27.94,
        waist_cm=27.94,
        hip_cm=27.94
    )

    result = compare_garment_with_wish(garment, wish, "inch")

    assert result.compared_count == 6
    assert result.unit == "inch"
    assert result.items[0].my_cloth == 10.0
    assert result.items[0].wish_cloth == 11.0
    assert result.items[0].diff == 1.0
    assert result.items[0].message == "내 옷보다 +1.0inch 큽니다"