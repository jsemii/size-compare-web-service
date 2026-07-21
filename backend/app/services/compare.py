from app.schemas.compare import CompareItem, CompareResponse

# 비교할 치수 컬럼 이름 목록
MEASUREMENT_FIELDS = [
    "total_length_cm",
    "shoulder_cm",
    "chest_cm",
    "sleeve_cm",
    "waist_cm",
    "hip_cm"
]

# 1인치 = 2.54cm
CM_PER_INCH = 2.54

def convert_unit(value: float | None, unit: str) -> float | None:
    """cm 값을 요청한 단위로 변환한다. 값이 없으면 None을 그대로 돌려준다."""
    if value is None:
        return None
    
    value = float(value)

    if unit == "inch":
        return round(value / CM_PER_INCH, 1)
    
    return round(value, 1)

def build_message(diff: float, unit: str) -> str:
    """차이값을 사람이 읽을 문장으로 바꾼다"""
    if diff > 0:
        return f"내 옷보다 +{diff}{unit} 큽니다"
    
    if diff < 0:
        return f"내 옷보다 {diff}{unit} 작습니다"
    
    return "내 옷과 같습니다"


def compare_garment_with_wish(garment, wish, unit: str = "cm") -> CompareResponse:
    """내 옷과 위시 상품의 치수를 항목별로 비교한다"""
    items = []
    compared_count = 0
    missing_count = 0

    for field_name in MEASUREMENT_FIELDS:
        my_raw = getattr(garment, field_name)
        wish_raw = getattr(wish, field_name)

        label = field_name.replace("_cm", "")

        if my_raw is None or wish_raw is None:
            missing_count += 1
            items.append(
                CompareItem(
                    field=label,
                    my_cloth=None,
                    wish_cloth=None,
                    diff=None,
                    message="치수 정보가 없습니다",
                    comparable=False,
                )
            )
            continue

        my_value = convert_unit(my_raw, unit)
        wish_value = convert_unit(wish_raw, unit)
        diff = round(wish_value - my_value, 1)

        compared_count += 1
        items.append(
            CompareItem(
                field=label,
                my_cloth=my_value,
                wish_cloth=wish_value,
                diff=diff,
                message=build_message(diff, unit),
                comparable=True,
            )
        )

    return CompareResponse(
        unit=unit,
        my_garment_name=garment.name,
        wish_item_name=wish.name,
        items=items,
        compared_count=compared_count,
        missing_count=missing_count,
    )