#!/usr/bin/env python3
"""Tier B enrichment — 상위 concept 신설 (기존 개별 concept은 유지).
각 section 맨 앞에 "상위 개념" concept을 prepend하여 types로 요약.

대상:
  01 소프트웨어 설계 & 아키텍처 / 소프트웨어 아키텍처 스타일 → "아키텍처 스타일 종류" 신설
  01 재사용 & 자료구조 / 자료구조(Data Structure) → "자료구조의 종류" 신설
  02 데이터 모델링 & ERD / 데이터 모델링의 절차 → "데이터 모델링 단계" 신설
  02 정규화 & 무결성 / 정규화와 이상현상 → "이상 현상" 신설
  02 정규화 & 무결성 / 정규화를 적용한 데이터베이스 설계-(5차 정규화) → "5차 정규화" 신설
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
JSON_DIR = ROOT / "topcit_json_v2"

SOURCE_01 = {
    "title": "TOPCIT ESSENCE ver.3 — 소프트웨어 개발",
    "note": "정보통신산업진흥원(NIPA) 공식 교재",
}
SOURCE_02 = {
    "title": "TOPCIT ESSENCE ver.3 — 데이터 이해와 활용",
    "note": "정보통신산업진흥원(NIPA) 공식 교재",
}


# ──────────────────────────────────────────────────────────────
# 신설할 상위 concept들
# 각 항목: (과목, chapter 제목, section 제목, 새 concept)
# ──────────────────────────────────────────────────────────────

NEW_CONCEPTS = [
    # ========== 01 소프트웨어 개발 ==========
    ("01", "소프트웨어 설계 & 아키텍처", "소프트웨어 아키텍처 스타일", {
        "title": "소프트웨어 아키텍처 스타일 종류",
        "keywords": ["아키텍처 스타일", "MVC", "클라이언트-서버", "계층 구조", "컨텍스트 모델"],
        "background": "소프트웨어 아키텍처를 구성하는 방식은 여러 가지 스타일로 정형화되어 있다. 어떤 스타일을 선택하느냐에 따라 시스템의 구조·품질 속성·확장성·유지보수성이 달라진다.",
        "explanation": "대표적인 아키텍처 스타일은 4가지로, 각 스타일은 해결하려는 문제와 제공하는 이점이 다르다. 아래 types에서 4종을 비교해 보자. 각 개별 스타일의 상세 학습은 이 section의 다른 카드를 참고.",
        "mnemonic": "【구분】4종 스타일: MVC(분리) · 클라이언트-서버(역할) · 계층(쌓기) · 컨텍스트(경계).",
        "priority": 2,
        "priority_evidence": "분류형_비교학습_상위요약",
        "types": {
            "caption": "대표적인 소프트웨어 아키텍처 스타일 4종. 각 스타일의 상세는 이 section 내 개별 카드에서.",
            "items": [
                {"name": "MVC 구조", "en": "Model-View-Controller",
                 "note": "애플리케이션을 Model(데이터·비즈니스 로직), View(화면 표현), Controller(사용자 입력 처리)의 3개로 분리하는 스타일. UI와 비즈니스 로직을 분리해 유지보수성·재사용성을 높인다. 웹 프레임워크의 표준 패턴."},
                {"name": "클라이언트-서버 모델", "en": "Client-Server",
                 "note": "역할을 서버(서비스 제공자)와 클라이언트(서비스 소비자)로 분리. 서버는 자원을 중앙 관리하고 클라이언트는 UI를 담당. 네트워크 분산 시스템의 기본 구조."},
                {"name": "계층 구조", "en": "Layered Architecture",
                 "note": "기능을 역할별로 여러 계층으로 쌓고, 각 계층은 바로 아래 계층만 호출. 표현·비즈니스·데이터 계층처럼 관심사를 분리해 구조를 명확히 한다. OSI 7계층이 대표 예."},
                {"name": "컨텍스트 모델", "en": "Context Model",
                 "note": "시스템과 외부 환경(사용자·다른 시스템·외부 장치)의 경계를 명확히 하는 모델. 시스템의 범위와 외부 인터페이스를 정의하여 요구사항 분석과 설계의 출발점이 된다."},
            ],
        },
        "sources": [SOURCE_01],
    }),

    ("01", "재사용 & 자료구조", "자료구조(Data Structure)", {
        "title": "자료구조의 종류",
        "keywords": ["자료구조", "선형", "비선형", "스택", "큐", "트리", "그래프"],
        "background": "컴퓨터가 데이터를 효율적으로 저장·처리하려면 용도에 맞는 자료구조를 선택해야 한다. 자료구조는 데이터 요소들의 배열 방식에 따라 선형/비선형으로 크게 나뉜다.",
        "explanation": "자료구조는 데이터가 순서대로 나열되는 선형 자료구조(배열/리스트/스택/큐/데크)와 계층·네트워크 형태로 확장되는 비선형 자료구조(트리/그래프)로 분류된다. 각 구조별 상세 학습은 이 section의 개별 카드를 참고.",
        "mnemonic": "【분류】선형 = 일렬(스택·큐·배열) / 비선형 = 가지(트리·그래프).",
        "priority": 2,
        "priority_evidence": "분류형_비교학습_상위요약",
        "types": {
            "caption": "자료구조는 데이터 배열 방식에 따라 선형과 비선형 2가지로 대분류된다. 각 sub-type의 상세는 개별 카드 참고.",
            "items": [
                {"name": "배열/리스트", "en": "Array / List (선형)",
                 "note": "선형 자료구조. 데이터를 일렬로 나열. 배열은 고정 크기·인덱스 기반 O(1) 접근, 리스트는 가변 크기·포인터 연결. DBMS 인덱스, 탐색·정렬 문제에 활용."},
                {"name": "스택", "en": "Stack (선형, LIFO)",
                 "note": "선형 자료구조. 후입선출(LIFO). 인터럽트 처리, 재귀 프로그램의 순서 제어, 서브루틴의 복귀 번지 저장, 후위 표기법 연산, 텍스트 에디터 Undo 기능 등에 활용."},
                {"name": "큐", "en": "Queue (선형, FIFO)",
                 "note": "선형 자료구조. 선입선출(FIFO). 운영체제의 작업 스케줄링, 대기 행렬 처리, 비동기 데이터 교환(파일I/O, Pipes, Sockets), 키보드 버퍼, 스풀 운용에 활용."},
                {"name": "데크", "en": "Deque (선형)",
                 "note": "선형 자료구조. 양쪽 끝에서 삽입·삭제가 가능한 '양방향 큐'. 스택과 큐의 장점을 모두 활용하여 스택/큐 관련 분야에서 쓰인다."},
                {"name": "트리", "en": "Tree (비선형)",
                 "note": "비선형 자료구조. 계층적 구조로 부모-자식 노드 관계. 탐색이나 정렬과 같은 문제, 문법의 파싱, 허프만 코드, 결정 트리, 게임 등에 활용."},
                {"name": "그래프", "en": "Graph (비선형)",
                 "note": "비선형 자료구조. 노드들이 에지로 자유롭게 연결. 컴퓨터 네트워크(근거리 통신망·인터넷·웹 등), 전기회로 분석, 이항 관계, 연립 방정식 등에 활용."},
            ],
        },
        "sources": [SOURCE_01],
    }),

    # ========== 02 데이터 이해와 활용 ==========
    ("02", "데이터 모델링 & ERD", "데이터 모델링의 절차", {
        "title": "데이터 모델링 단계",
        "keywords": ["데이터 모델링", "개념적", "논리적", "물리적", "모델링 절차"],
        "background": "데이터베이스 설계는 추상 수준에서 구체 수준으로 단계적으로 진행된다. 각 단계마다 다루는 대상과 산출물, 주된 결정 사항이 다르다. 이 흐름을 알아야 DB 설계 전 과정을 체계적으로 수행할 수 있다.",
        "explanation": "데이터 모델링은 개념적 → 논리적 → 물리적 3단계로 진행된다. 상위 단계일수록 추상적이고 DBMS와 독립적이며, 하위 단계일수록 구체적이고 특정 DBMS·하드웨어에 종속된다. 각 단계의 상세는 이 section의 개별 카드를 참고.",
        "mnemonic": "【순서】개념 → 논리 → 물리. '업무 이해 → 테이블 스키마 → 실제 저장 구조'의 3단계 깔때기.",
        "priority": 2,
        "priority_evidence": "분류형_비교학습_상위요약",
        "types": {
            "caption": "데이터 모델링의 3단계. 추상에서 구체로 진행되며 각 단계의 산출물이 다음 단계의 입력이 된다.",
            "items": [
                {"name": "개념적 모델링", "en": "Conceptual Modeling",
                 "note": "1단계. 업무 도메인을 파악하고 주요 엔터티·관계를 식별한다. DBMS와 무관하게 '무엇을' 관리할지를 정의. 주 산출물: ER 다이어그램. 현업·경영진과의 소통 도구."},
                {"name": "논리적 모델링", "en": "Logical Modeling",
                 "note": "2단계. 개념 모델을 관계형 스키마로 변환하고 정규화를 수행. 테이블·칼럼·관계·키를 구체적으로 정의. DBMS 제품과는 여전히 독립적. 주 산출물: 논리 데이터 모델·정규화된 테이블 스키마."},
                {"name": "물리적 모델링", "en": "Physical Modeling",
                 "note": "3단계. 특정 DBMS와 하드웨어를 고려해 저장 구조·인덱스·파티션·반정규화 등을 결정. 성능·용량·보안 요구사항이 반영된다. 주 산출물: 물리 데이터 모델·DDL 스크립트."},
            ],
        },
        "sources": [SOURCE_02],
    }),

    ("02", "정규화 & 무결성", "정규화와 이상현상", {
        "title": "이상 현상",
        "keywords": ["이상 현상", "삽입 이상", "삭제 이상", "수정 이상", "갱신 이상", "정규화"],
        "background": "정규화되지 않은 테이블은 데이터 중복 때문에 삽입·삭제·수정 시 원치 않는 부작용이 발생한다. 이를 '이상 현상(Anomaly)'이라 부르며, 정규화의 필요성을 설명하는 핵심 근거다.",
        "explanation": "이상 현상은 크게 3가지 — 삽입 이상, 삭제 이상, 수정 이상(갱신 이상). 원인은 모두 한 테이블에 여러 정보가 섞여 중복으로 저장되기 때문이며, 해결은 정규화로 테이블을 의미 단위로 분해하는 것이다. 각 이상의 상세 예시는 이 section의 개별 카드에서.",
        "mnemonic": "【3종】삽입/삭제/수정 — '넣으려다 문제, 지우려다 문제, 고치려다 문제'. 원인은 중복, 해결은 정규화.",
        "priority": 1,
        "priority_evidence": "분류형_비교학습_상위요약_핵심빈출",
        "types": {
            "caption": "관계형 DB에서 정규화가 되지 않았을 때 발생하는 3가지 이상 현상. 정규화의 목적은 이 현상들을 제거하는 것.",
            "items": [
                {"name": "삽입 이상", "en": "Insertion Anomaly",
                 "note": "새 데이터를 삽입하려는데 관련 없는 다른 속성 값까지 함께 입력하지 않으면 삽입이 불가능한 현상. 예: '학생-과목' 합쳐진 테이블에 수강 신청 없는 신입생을 등록하려면 임의의 과목 정보까지 입력해야 하는 문제."},
                {"name": "삭제 이상", "en": "Deletion Anomaly",
                 "note": "특정 튜플을 삭제했는데 의도하지 않은 다른 정보까지 함께 삭제되는 현상. 예: 한 학생의 수강 기록이 유일한 상태에서 그 기록을 지우면 해당 과목 정보 자체가 사라지는 문제."},
                {"name": "수정 이상 (갱신 이상)", "en": "Update Anomaly",
                 "note": "중복 저장된 데이터 중 일부만 수정되어 데이터의 일관성이 깨지는 현상. 예: 한 과목명이 여러 행에 중복 저장되어 있을 때, 일부 행만 수정하면 같은 과목이 서로 다른 이름으로 존재하게 되는 문제."},
            ],
        },
        "sources": [SOURCE_02],
    }),

    ("02", "정규화 & 무결성", "정규화를 적용한 데이터베이스 설계-(5차 정규화)", {
        "title": "5차 정규화",
        "keywords": ["5차 정규화", "5NF", "조인 종속", "Join Dependency"],
        "background": "5차 정규화(5NF)는 4차 정규화 이후 남아 있는 조인 종속(Join Dependency)을 제거하기 위한 최종 정규화 단계다. 실무에서는 드물게 나타나지만, 다대다 관계가 얽혀 있는 경우 반드시 고려해야 한다.",
        "explanation": "5NF는 모든 조인 종속이 후보키에 의해서만 성립하도록 테이블을 분해한 상태다. 개념·특징·수행 방법의 세부는 이 section의 개별 카드에서.",
        "mnemonic": "【핵심】5NF = 조인 종속 제거. '후보키를 통하지 않은 조인 종속이 없는 상태'.",
        "priority": 3,
        "priority_evidence": "분류형_비교학습_상위요약",
        "types": {
            "caption": "5차 정규화를 3가지 측면(개념·특징·수행)으로 나누어 정리.",
            "items": [
                {"name": "개념", "en": "Concept",
                 "note": "4차 정규형(4NF) 상태에서 후보키를 통하지 않은 조인 종속(Join Dependency, JD)을 제거한 것. 릴레이션을 여러 릴레이션으로 분해했다가 다시 조인해도 원래 릴레이션이 손실 없이 복원되어야 한다(무손실 조인)."},
                {"name": "특징", "en": "Properties",
                 "note": "모든 속성이 주식별자(후보키)인 All-Key 릴레이션에서 주로 성립. 의미적 연관성 제약(Constraint)이 있어야 분해 가능. 3개 이상의 속성이 연관된 다치 종속이 아닌 조인 종속에 해당. 실무 적용은 드물지만 최고 수준의 정규화."},
                {"name": "수행", "en": "Procedure",
                 "note": "① 조인 종속 관계 식별 → ② 후보키를 통하지 않은 조인 종속 발견 → ③ 해당 관계를 기준으로 릴레이션 분해 → ④ 분해된 릴레이션들을 조인해 원본과 일치하는지 검증. 사원-기술-프로젝트 같은 3자 관계에서 적용 사례가 많다."},
            ],
        },
        "sources": [SOURCE_02],
    }),
]


def prepend_concept(data, chapter_title, section_title, new_concept):
    """해당 section 맨 앞에 new_concept을 삽입. 이미 동명 concept이 있으면 types만 덮어쓰기."""
    for ch in data["chapters"]:
        if ch["title"] != chapter_title:
            continue
        for sec in ch["sections"]:
            if sec["title"] != section_title:
                continue
            # 동명 concept 이미 존재하는지 확인
            for i, con in enumerate(sec["concepts"]):
                if con.get("title") == new_concept["title"]:
                    # 덮어쓰기 (types/sources만 업데이트)
                    sec["concepts"][i] = new_concept
                    return "updated"
            sec["concepts"].insert(0, new_concept)
            return "inserted"
    return "section not found"


def main():
    results = []
    for subj, ch_title, sec_title, new_con in NEW_CONCEPTS:
        path = JSON_DIR / f"topcit_{subj}.json"
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        r = prepend_concept(data, ch_title, sec_title, new_con)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        results.append((subj, new_con["title"], r))

    print("=== Tier B 상위 concept 신설 결과 ===")
    for subj, title, r in results:
        mark = "✓" if r in ("inserted", "updated") else "✗"
        print(f"  {mark} [{subj}] {title} — {r}")


if __name__ == "__main__":
    main()
