#!/usr/bin/env python3
"""topcit_01.json 챕터 재구조화"""
import json
from pathlib import Path

PATH = Path(__file__).parent / "topcit_json_v2" / "topcit_01.json"

with open(PATH, encoding="utf-8") as f:
    data = json.load(f)

# 모든 섹션을 제목으로 조회 가능하게 플랫화
all_sections = {
    sec["title"]: sec
    for ch in data["chapters"]
    for sec in ch["sections"]
}

def secs(*titles):
    result = []
    for t in titles:
        if t in all_sections:
            result.append(all_sections[t])
        else:
            print(f"  [경고] 섹션 없음: {t}")
    return result

new_chapters = [
    {
        "title": "소프트웨어 공학 기초",
        "sections": secs(
            "소프트웨어 공학의 배경과 목적",
            "소프트웨어 개발 생명주기",
            "애자일 개발 방법론",
        )
    },
    {
        "title": "소프트웨어 설계 & 아키텍처",
        "sections": secs(
            "소프트웨어 설계 원리",
            "소프트웨어 아키텍처 스타일",
            "소프트웨어 아키텍처 설계",
            "소프트웨어 아키텍처 설계 표현 방법",
            "구조적 설계 방법",
            "객체 지향 설계와 원리",
            "디자인 패턴",
        )
    },
    {
        "title": "UI/UX & 개발 도구",
        "sections": secs(
            "사용자 인터페이스(User Interface) 개요",
            "사용자 경험(User Experience) 개요",
            "프로그래밍 언어의 개요",
            "소프트웨어 개발 프레임워크",
            "통합개발환경(IDE)",
            "소프트웨어 개발도구와 프로그래밍 언어의 기술 동향",
            "개발프레임워크와 소프트웨어 아키텍처 기술 동향",
        )
    },
    {
        "title": "품질 & 요구사항",
        "sections": secs(
            "테스팅 개념 및 프로세스",
            "리팩토링",
            "요구사항 관리",
            "요구사항 명세",
        )
    },
    {
        "title": "형상관리 & 오픈소스",
        "sections": secs(
            "형상관리 도구",
            "소프트웨어 형상관리의 개요",
            "형상관리 개념도 및 구성 요소",
            "오픈소스 소프트웨어 라이선스",
            "오픈소스 소프트웨어 개념",
        )
    },
    {
        "title": "소프트웨어 유지보수",
        "sections": secs(
            "소프트웨어 유지보수의 개념과 유형",
            "소프트웨어 유지보수 활동",
        )
    },
    {
        "title": "재사용 & 자료구조",
        "sections": secs(
            "소프트웨어 재사용",
            "자료구조(Data Structure)",
        )
    },
]

# 빈 섹션 챕터 제거
new_chapters = [ch for ch in new_chapters if ch["sections"]]

data["chapters"] = new_chapters

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"완료: {len(new_chapters)}개 챕터")
for ch in new_chapters:
    secs_count = len(ch["sections"])
    cons_count = sum(len(s["concepts"]) for s in ch["sections"])
    print(f"  [{ch['title']}] {secs_count}섹션 {cons_count}개념")
