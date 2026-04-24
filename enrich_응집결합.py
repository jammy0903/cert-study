#!/usr/bin/env python3
"""topcit_01.json의 응집도·결합도 개념에 `types` 필드를 추가한다.
출처: topcit_texts/topcit_01.txt (TOPCIT ESSENCE ver.3, 소프트웨어 개발, pp.53~55)
"""
import json
from pathlib import Path

PATH = Path(__file__).parent / "topcit_json_v2" / "topcit_01.json"

COHESION_TYPES = {
    "caption": "응집도는 모듈 내부 구성 요소들이 공통 목적 달성을 위해 얼마나 관련되어 있는지를 나타내는 모듈 성숙도의 측정치다. 강할수록 모듈이 단일 기능으로 뭉쳐 있어 독립성이 높다.",
    "scale": "strong-to-weak",
    "items": [
        {"name": "기능적 응집도", "en": "Functional Cohesion", "tier": "strong",
         "note": "모듈 내부의 모든 기능 요소들이 단일 문제와 연관되어 수행될 경우의 응집도. 가장 이상적."},
        {"name": "순차적 응집도", "en": "Sequential Cohesion", "tier": "strong",
         "note": "모듈 내 하나의 활동으로부터 나온 출력 데이터를 그 다음 활동의 입력 데이터로 사용할 경우의 응집도."},
        {"name": "교환적(통신적) 응집도", "en": "Communicational Cohesion", "tier": "mid",
         "note": "동일한 입력과 출력을 사용하여 서로 다른 기능을 수행하는 구성 요소들이 모인 경우의 응집도."},
        {"name": "절차적 응집도", "en": "Procedural Cohesion", "tier": "mid",
         "note": "모듈이 다수의 관련 기능을 가질 때, 모듈 안의 구성 요소들이 그 기능을 순차적으로 수행할 경우의 응집도."},
        {"name": "시간적 응집도", "en": "Temporal Cohesion", "tier": "mid",
         "note": "특정 시간에 처리되는 몇 개의 기능을 모아 하나의 모듈로 작성할 경우의 응집도."},
        {"name": "논리적 응집도", "en": "Logical Cohesion", "tier": "weak",
         "note": "유사한 성격을 갖거나 특정 형태로 분류되는 처리 요소들로 하나의 모듈이 형성되는 경우의 응집도."},
        {"name": "우연적 응집도", "en": "Coincidental Cohesion", "tier": "weak",
         "note": "모듈 내부의 각 구성 요소들이 서로 관련 없는 요소로만 구성된 경우의 응집도. 가장 바람직하지 않음."},
    ],
}

COUPLING_TYPES = {
    "caption": "결합도는 모듈 사이의 상호 연관성의 복잡도다. 약할수록 한 모듈의 변경이 다른 모듈에 미치는 영향(파문 효과)이 작아 유지보수가 쉽다.",
    "scale": "weak-to-strong",
    "items": [
        {"name": "자료 결합도", "en": "Data Coupling", "tier": "weak",
         "note": "모듈 간 인터페이스가 자료 요소(매개변수, 인수)로만 구성될 때의 결합도. 한 모듈의 내용을 변경해도 다른 모듈에 영향이 없는 가장 바람직한 결합도."},
        {"name": "스탬프 결합도", "en": "Stamp Coupling", "tier": "weak",
         "note": "모듈 간 인터페이스로 배열이나 레코드 등 자료 구조가 전달될 때의 결합도. 자료 구조의 변화가 해당 필드를 실제로 사용하지 않는 모듈에까지 영향을 미칠 수 있다."},
        {"name": "제어 결합도", "en": "Control Coupling", "tier": "mid",
         "note": "한 모듈에서 다른 모듈로 논리적인 흐름을 제어하는 제어 요소(Function Code, Switch, Tag, Flag)가 전달될 때의 결합도. 상위 모듈이 하위 모듈의 상세 처리 절차를 알고 통제하는 구조에서 발생."},
        {"name": "외부 결합도", "en": "External Coupling", "tier": "mid",
         "note": "어떤 모듈에서 외부로 선언한 데이터(변수)를 다른 모듈에서 참조할 때의 결합도. 참조되는 데이터의 범위를 각 모듈에서 제한할 수 있다."},
        {"name": "공통(공유) 결합도", "en": "Common Coupling", "tier": "strong",
         "note": "공유되는 공통 데이터 영역을 여러 모듈이 사용할 때의 결합도. 공통 데이터 영역을 조금만 변경해도 이를 사용하는 모든 모듈에 영향을 미쳐 독립성을 약하게 만든다."},
        {"name": "내용 결합도", "en": "Content Coupling", "tier": "strong",
         "note": "한 모듈이 다른 모듈의 내부 기능 및 내부 자료를 직접 참조하거나 수정할 때의 결합도. 가장 강한 결합도로 피해야 한다."},
    ],
}

SOURCE = {
    "title": "TOPCIT ESSENCE ver.3 — 소프트웨어 개발 (pp.53~55)",
    "note": "정보통신산업진흥원(NIPA) 공식 교재",
}


def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)

    updated = []
    for ch in data["chapters"]:
        for sec in ch["sections"]:
            for con in sec["concepts"]:
                if con["title"] == "응집도":
                    con["types"] = COHESION_TYPES
                    con.setdefault("sources", []).append(SOURCE)
                    updated.append("응집도")
                elif con["title"] == "결합도":
                    con["types"] = COUPLING_TYPES
                    con.setdefault("sources", []).append(SOURCE)
                    updated.append("결합도")

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"enriched: {updated}")


if __name__ == "__main__":
    main()
