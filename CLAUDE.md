# cert-study — 자격증 대비 학습 자료 저장소

정보처리기사·TOPCIT 등 IT 자격증 대비 학습 자료를 모아둔 저장소. TOPCIT 6과목 레슨 뷰어가 핵심 산출물.

## 메인 산출물

### 📘 TOPCIT 레슨 뷰어 (`topcit_lesson/`)
- **입구:** `topcit_lesson/index.html` — 6과목 인덱스
- **과목별 페이지:** `topcit_lesson/0N/index.html` (01~06)
- hankuksa 프로젝트 스타일의 풀스크린 레슨 뷰어
- 카드 뷰 + 검색 + 챕터 탭 + 우선순위 필터(P1~P4)
- 카드 → 풀스크린 레슨 (배경 → 핵심 설명 → 유형 → 5초 암기 → 완료)
- 키보드 ←/→/Esc + 버튼 네비 (모바일 스와이프는 제거)

### 🎯 분류형 개념 types 필드 (130개)
모든 분류형 개념이 "상위 개념 + 하위 유형 리스트"로 렌더됨. 예:
- 응집도 → 기능적/순차적/교환적/절차적/시간적/논리적/우연적 (7종, 강약 tier)
- 결합도 → 자료/스탬프/제어/외부/공통/내용 (6종, 약강 tier)
- RAID → 0/1/5/6/10
- ACID → 원자성/일관성/격리성/지속성
- 기타 126개

## 프로젝트 구조

```
cert-study/
├── CLAUDE.md                    # 이 파일 (프로젝트 가이드)
├── TYPES_ENRICHMENT_PLAN.md     # 분류형 개념 enrichment 계획 & 규칙 (self-contained)
├── index.html                   # 메인 인덱스 (TOPCIT 뷰어·퀴즈·개념집 진입점)
├── memory-frame.css             # 공통 스타일
│
├── gen_topcit.py                # 📌 HTML 생성기 (JSON → topcit_lesson/)
├── enrich_응집결합.py            # 응집도·결합도 enrichment (샘플)
├── enrich_topcit_01.py          # 01 소프트웨어 개발 enrichment (16개)
├── enrich_topcit_02.py          # 02 데이터 enrichment (25개)
├── enrich_topcit_03.py          # 03 시스템 아키텍처 enrichment (40개)
├── enrich_topcit_04.py          # 04 정보보안 enrichment (18개)
├── enrich_topcit_05.py          # 05 IT 비즈니스 enrichment (12개)
├── enrich_topcit_06.py          # 06 커뮤니케이션·PM enrichment (14개)
├── enrich_topcit_tier_b.py      # Tier B 상위 concept 신설 (5개)
├── scan_types_candidates.py     # 분류형 후보 자동 스캐너
│
├── topcit_json_v2/              # 개념 데이터 (정규화됨)
│   ├── topcit_01.json ~ topcit_06.json   # 과목별 개념
│   └── topcit_exam.json                  # 기출 퀴즈 데이터
│
├── topcit_texts/                # 원본 교재 OCR 텍스트 (enrichment 출처)
│   └── topcit_01.txt ~ topcit_06.txt
│
├── topcit_essence/              # 원본 교재 PDF
│
├── topcit_lesson/               # ✨ 생성된 레슨 뷰어 (gen_topcit.py 산출물)
│   ├── index.html
│   └── 01/ ~ 06/
│
├── topcit_concepts.html         # 커리큘럼 + 우선순위 개념집
├── topcit_quiz.html             # TOPCIT 기출 퀴즈
├── topcit_exam_images/          # 퀴즈 이미지
│
└── 정보처리기사_실기_*.html      # 정보처리기사 실기 암기 프레임 (DB/네트워크/보안)
```

## 주요 작업 흐름

### 레슨 뷰어 재생성
```bash
python3 gen_topcit.py
```
JSON에 변경이 있으면 반드시 실행하여 `topcit_lesson/` 재생성.

### 개념에 types(하위 유형) 추가
1. `TYPES_ENRICHMENT_PLAN.md` §3 스펙 확인
2. `topcit_texts/topcit_0N.txt`에서 원본 인용
3. `enrich_topcit_0N.py`에 entry 추가 또는 새 enrich 스크립트 생성
4. 실행 → `gen_topcit.py` 재생성 → 브라우저 확인

### 로컬 미리보기
```bash
python3 server.py  # 또는 python3 -m http.server
```

## 중요 문서

- **`TYPES_ENRICHMENT_PLAN.md`** — 분류형 개념 enrichment 규칙·스펙·체크리스트. self-contained. 새 분류형 개념 추가 시 반드시 참조.
- **`topcit_기출_분석.md`** — 기출 31문항 분석 및 학습 우선순위

## 가이드라인

- **JSON 편집은 Edit 도구보다 Python 스크립트로.** indent·escape 실수로 깨지기 쉬움. `enrich_topcit_01.py` 패턴 참고.
- **원본 인용 원칙.** enrichment는 반드시 `topcit_texts/topcit_0N.txt`에서 인용. 감으로 작성 금지.
- **기존 필드 보존.** 새 필드 추가 시 기존 구조를 깨지 않는다.
- **OCR 훼손 허용.** 원본 텍스트는 PDF OCR이라 깨진 글자가 많음. 의미가 명확한 수준에서 교정하되 추정 금지.
