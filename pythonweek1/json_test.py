import json
from pydantic import BaseModel, ValidationError
# 定义我们希望得到的数据结构
class WeatherArgs(BaseModel):
    city: str
    days: int
def parse_data(raw):
    try:
        data = json.loads(raw)
        result = WeatherArgs.model_validate(
            data,
            strict=True
        )

        return result

    except json.JSONDecodeError:
        print("错误：非法 JSON")

    except ValidationError as e:
        print("错误：字段缺失或类型错误")
        print(e)

    return None


test_cases = [
    '{"city":"西安","days":3}',
    '{"city":"西安"}',
    '{"city":"西安","days":"三天"}',
    '{"city":"西安",}'
]

for case in test_cases:
    print("\n输入：", case)
    print("解析结果：", parse_data(case))