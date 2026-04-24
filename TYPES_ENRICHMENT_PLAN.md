# TOPCIT 분류형 개념 Enrichment 작업 계획 & 규칙

**이 문서 하나만 보면 다음 AI 세션이 바로 이어받아 작업할 수 있게 구성됨.**
작업 중단 시 "현재 진행 상태" 섹션만 업데이트하고 종료. 재개 시 거기서부터.

---

## 0. 빠른 시작 (TL;DR)

1. **이 문서 전체를 먼저 읽는다.** 특히 §2 절대 규칙, §3 JSON 필드 스펙.
2. §9 "현재 진행 상태"에서 다음 작업 대상 개념을 확인한다.
3. `topcit_texts/topcit_0N.txt`에서 해당 개념의 원본 텍스트를 찾는다 (예: `grep -n "응집도의 종류" topcit_texts/topcit_01.txt`).
4. 원본에서 하위 유형 enumerate를 찾아 `types` 배열을 만든다.
5. `topcit_json_v2/topcit_0N.json`에서 해당 개념을 찾아 `types` + `sources` 필드를 추가한다.
6. `python3 gen_topcit.py`를 돌려 HTML 재생성.
7. `topcit_lesson/0N/index.html`에서 해당 개념 카드 클릭 → 유형 섹션이 렌더되는지 확인.
8. §9 상태 업데이트 후 다음 개념으로 이동.

---

## 1. 작업 목적

TOPCIT 개념 중 "상위 개념 + 하위 유형 나열"이 필요한 분류형 개념을 전수 enrichment한다.
응집도 → 7종 응집도, 결합도 → 6종 결합도처럼, 설명을 읽을 때 하위 유형들이 **같이** 보여야 학습이 된다.
현재 JSON은 상위 개념만 있고 하위 유형이 빠져 있어, 읽어도 "그래서 뭐가 있는데?"로 끝나는 문제가 있다.

## 2. 절대 규칙

- **감으로 쓰지 않는다.** 반드시 `topcit_texts/topcit_0N.txt` 원본에서 인용한다.
- **외부 지식을 임의로 덧붙이지 않는다.** 원본에 없는 유형은 추가하지 않는다.
- **OCR 깨짐 허용.** 원본 텍스트는 PDF OCR이라 글자가 깨진 경우가 많다. 의미가 명확한 수준에서 교정하되, 추정 금지. 너무 깨져 있으면 skip하고 TODO로 남긴다.
- **순서 유지.** 원본에 나열 순서(강→약, 약→강 등)가 있으면 그대로 따른다.
- **한 개념씩 진행.** 한 번에 여러 개 묶어 치지 않는다. 검수 사이클을 짧게 유지.
- **DB/다른 프로젝트 건드리지 않는다.** 수정 범위는 `topcit_json_v2/*.json`과 `gen_topcit.py`만.
- **기존 필드 구조를 깨지 않는다.** `types`는 기존 필드에 추가되는 것이고, 다른 필드는 그대로 둔다.

## 3. JSON 필드 스펙 (`types`)

### 3-1. 형식

```json
"types": {
  "caption": "상위 개념의 한 줄 정의/맥락. (1~2문장)",
  "scale": "strong-to-weak",   // 또는 "weak-to-strong", 없으면 생략
  "items": [
    {
      "name": "기능적 응집도",
      "en": "Functional Cohesion",
      "tier": "strong",         // 'strong' | 'mid' | 'weak' | 생략
      "note": "모듈 내부의 모든 기능 요소들이 단일 문제와 연관되어 수행될 경우의 응집도."
    }
  ]
}
```

또는 **배열만** 써도 됨(caption/scale 불필요 시):

```json
"types": [
  { "name": "...", "en": "...", "note": "..." },
  ...
]
```

### 3-2. 필드 의미

| 필드 | 필수 | 설명 |
|---|---|---|
| `caption` | 선택 | 상위 개념의 한 줄 요약. 유형 리스트 위에 설명으로 렌더됨 |
| `scale` | 선택 | `strong-to-weak` 또는 `weak-to-strong`. 강도 스케일 바 렌더 |
| `items` | 필수 | 하위 유형 배열 |
| `items[].name` | 필수 | 한글 이름 (예: "기능적 응집도") |
| `items[].en` | 선택 | 영문 이름 (예: "Functional Cohesion") |
| `items[].tier` | 선택 | `strong`/`mid`/`weak` — 배지 색상에 사용. 강도 개념이 없으면 생략 |
| `items[].note` | 필수 | 원본 기반 정의 (1~3문장) |

### 3-3. `sources` 같이 추가 (필수)

모든 enrichment는 다음 출처 객체를 `sources` 배열에 push한다 (이미 있으면 중복 추가 금지):

```json
{
  "title": "TOPCIT ESSENCE ver.3 — {과목명} (pp.{페이지})",
  "note": "정보통신산업진흥원(NIPA) 공식 교재"
}
```

페이지 번호는 원본 `topcit_texts/topcit_0N.txt`에서 `TOPCIT ESSENCE` 근처에 있는 숫자(쪽번호)를 찾아서 쓴다. 못 찾으면 페이지 생략 OK.

## 4. 파일 위치 (변경 범위)

| 경로 | 역할 | 수정? |
|---|---|---|
| `topcit_json_v2/topcit_0N.json` | 개념 데이터. `types` 필드 추가 대상 | ✏️ 수정 |
| `topcit_texts/topcit_0N.txt` | 원본 교재 OCR 텍스트. 인용 소스 | 📖 읽기만 |
| `gen_topcit.py` | HTML 생성기. `types` 렌더링 이미 구현됨 | ❌ 수정 금지 (버그 발견 시 예외) |
| `topcit_lesson/0N/index.html` | 생성된 결과물. 검증용 | 🔄 재생성만 |
| `TYPES_ENRICHMENT_PLAN.md` | 이 문서. 진행 상태 업데이트 | 📝 상태만 |

## 5. 작업 절차 (개념 1개 단위)

1. §9에서 다음 대상 개념을 고른다 (`[ ]`).
2. 원본 텍스트에서 위치 찾기:
   ```bash
   grep -n "개념명" topcit_texts/topcit_0N.txt
   ```
   또는 섹션 힌트로 `grep -n "종류에는"`, `grep -n "유형"` 등.
3. 해당 부분 전후 30~60줄을 읽어 원문을 확보한다:
   ```bash
   sed -n '{start},{end}p' topcit_texts/topcit_0N.txt
   ```
4. `types` 객체를 초안 작성한다. §3 스펙 준수.
   - OCR 깨진 글자 교정 (예: `SUS` → `응집도`, 명백할 때만).
   - 원본 설명을 최대한 그대로 옮긴다. 윤색 최소화.
5. enrichment Python 스크립트를 작성/업데이트해서 JSON 수정:
   - 템플릿: `enrich_응집결합.py` 참고
   - 개념명으로 탐색해서 `con["types"] = {...}`와 `sources.append(SOURCE)` (중복 방지)
   - JSON 덮어쓰기: `json.dump(data, f, ensure_ascii=False, indent=2)`
6. 실행:
   ```bash
   python3 {enrichment_script}.py
   python3 gen_topcit.py
   ```
7. 결과 확인:
   ```bash
   grep -o "{items[0].en}" topcit_lesson/0N/index.html  # 렌더 확인
   ```
   브라우저에서 `topcit_lesson/0N/index.html` 열어 해당 카드 클릭, 유형 섹션이 보이는지 확인.
8. §9 상태 업데이트 (`[x]`로 체크).
9. 필요 시 commit (사용자 지시가 있을 때만).

## 6. JSON 편집 팁 (안전한 방식)

- **Edit 도구로 직접 JSON 편집 지양.** indent·escape 실수로 깨지기 쉬움.
- **Python 스크립트로 JSON 편집 권장.** `enrich_응집결합.py`가 기준 템플릿.
- 한 과목 내 여러 개념을 한 번에 처리하려면 스크립트에 딕셔너리로 나열:
  ```python
  ENRICHMENTS = {
      "응집도": {"caption": ..., "items": [...]},
      "결합도": {"caption": ..., "items": [...]},
      ...
  }
  for target_title, types_data in ENRICHMENTS.items():
      for ch in data["chapters"]:
          for sec in ch["sections"]:
              for con in sec["concepts"]:
                  if con["title"] == target_title:
                      con["types"] = types_data
                      ...
  ```
- **한 과목 끝나면 스크립트 파일은 `enrich_topcit_0N.py` 같은 이름으로 남기고 커밋.** 나중에 재현 가능하게.

## 7. 검증 체크리스트 (개념마다)

- [ ] 원본 텍스트에서 유형 이름과 순서가 실제로 확인되는가
- [ ] `items[].note`가 원본 설명과 의미적으로 일치하는가 (윤색 말고 인용에 가깝게)
- [ ] `tier`가 원본 스케일(강도/중요도)과 일치하는가 — 없는 개념에는 tier 생략
- [ ] `sources`에 교재 출처가 추가되었는가 (중복 없는지)
- [ ] `gen_topcit.py` 실행 시 에러 없이 생성되는가
- [ ] 결과 HTML에 유형 섹션이 실제로 렌더되는가 (grep으로 영문명 확인)
- [ ] 기존 필드(background, explanation, mnemonic, priority 등) 그대로 보존되는가

## 8. Tier 분류 기준

- **Tier A** — 단일 개념이 이미 JSON에 있음. `types` 필드만 추가하면 끝.
- **Tier B** — 하위 유형들이 이미 별도 concept으로 쪼개져 있음. 상위 concept 신설 or 묶기 필요.
  Tier A 전부 끝난 뒤 재검토.
- **Tier D** — 완료.

---

## 9. 현재 진행 상태 (체크리스트)

> **다음 작업 대상은 이 섹션에서 첫 번째 `[ ]` 항목.**

### 01 소프트웨어 개발 ✅ Tier A 완료

Tier D (완료):
- [x] 응집도 — 7종 (기능적/순차적/교환적/절차적/시간적/논리적/우연적)
- [x] 결합도 — 6종 (자료/스탬프/제어/외부/공통/내용)
- [x] 소프트웨어 공학의 4가지 중요요소 — 방법/도구/절차/사람
- [x] 소프트웨어 생명주기 모델 종류 — V / VP(V+Prototyping) / 점증적 / 진화
- [x] 애자일 방법론 종류 — 스크럼/XP/린/AUP
- [x] 테스팅 유형 — 단위/통합/시스템/인수
- [x] 테스팅 기법 — 화이트박스/블랙박스 (2 범주, 각 sub-techniques)
- [x] 대표적인 리팩토링 기법 — Extract/Rename/Pull Up 등 10가지
- [x] 요구사항 명세 기법 — VDM/FSM/SADT/Usecase/Decision Table/ER (정형+비정형)
- [x] 소프트웨어 유지보수의 종류 — 수정/적응/완전화 (사유 기준). 시간/대상은 caption.
- [x] 소프트웨어 조직 유형 — 작업 형태/애플리케이션 분야/생명주기
- [x] 대표적인 디자인 패턴 — 생성/구조/행위 3범주 (GoF 23개)
- [x] 자료구조의 선택 기준 — 처리시간/크기/활용빈도
- [x] 알고리즘 분석 기준 — 정확성/작업량/기억장소/단순성/최적성
- [x] 형상관리의 구성요소 — 기준선/형상항목/형상제품/형상정보 (활동 4가지는 caption에)
- [x] 오픈소스 소프트웨어 라이선스 비교 — GPL 2/3, LGPL, MPL, Apache, BSD (엄격도 tier)

Tier B (완료):
- [x] **소프트웨어 아키텍처 스타일 종류** 상위 concept 신설 (기존 MVC/클라이언트-서버/계층/컨텍스트 카드 유지)
- [x] **자료구조의 종류** 상위 concept 신설 (선형/비선형 분류 + 6종, 기존 스택/큐/트리/그래프 카드 유지)

### 02 데이터 이해와 활용 ✅ Tier A 완료

Tier D (완료):
- [x] 주요 데이터베이스 유형 — 계층/네트워크/관계/객체지향/객체관계
- [x] 엔터티의 분류 — 유무형(3) + 발생시점(3)
- [x] 속성의 분류 — 기본/설계/파생
- [x] 식별자의 분류 — 대표성/생성여부/속성수/대체여부 4기준 × 각 2
- [x] 암스트롱의 추론 규칙 — 재귀/부가/이행 + 연합/분해/의사이행
- [x] 정규화 — 1NF/2NF/3NF/BCNF/4NF/5NF
- [x] 데이터 투명성 — 분할/위치/중복/장애/병행
- [x] 주요 빅데이터 분석 방법 — 로지스틱/의사결정트리/신경망/텍스트마이닝/SNA/오피니언마이닝/NLP
- [x] NoSQL의 저장방식 — Key-Value/Column Family/Document/Graph
- [x] NoSQL 데이터 모델의 특징 — BASE 기반/중복 통한 빠른 읽기/화면·로직 고려 설계
- [x] 데이터 정의어의 종류 — CREATE/ALTER/DROP/RENAME
- [x] DML 기본 연산 — SELECT/INSERT/UPDATE/DELETE
- [x] 데이터 제어어의 종류 — GRANT/REVOKE/DENY/COMMIT/ROLLBACK
- [x] 순수관계연산 — Select(σ)/Project(π)/Join(⋈)/Division(÷)
- [x] 일반집합연산 — 합집합/교집합/차집합/카티션 프로덕트
- [x] 인덱스 구조의 유형 — 트리/함수/비트맵조인/도메인
- [x] 트랜잭션의 ACID 특징 — 원자성/일관성/격리성/지속성
- [x] 동시성(병행) 제어를 하지 않았을 경우 발생하는 문제점 — 갱신손실/오손읽기/모순성/연쇄복귀/반복불가능읽기
- [x] 교착상태 발생원인 — 상호배제/점유대기/비선점/환형대기
- [x] 데이터베이스 장애(실패)의 유형 — 트랜잭션/시스템/디스크/사용자
- [x] 데이터베이스 복구 조치 유형 — REDO/UNDO
- [x] 데이터베이스 복구 기법 — 로그기반/검사점/그림자페이징
- [x] 데이터베이스 백업 방식의 종류와 특징 — 콜드/핫 + 전체/차등/증분/아카이브 로그
- [x] 기준에 따른 옵티마이저의 유형 — RBO/CBO
- [x] 데이터 품질관리 성숙모형 — 품질기준/관리 프로세스/성숙수준

Tier B (완료):
- [x] **이상 현상** 상위 concept 신설 (삽입/삭제/수정 3종, 기존 개별 카드 유지)
- [x] **데이터 모델링 단계** 상위 concept 신설 (개념적/논리적/물리적, 기존 개별 카드 유지)
- [x] **5차 정규화** 상위 concept 신설 (개념/특징/수행, 기존 개별 카드 유지)

### 03 시스템 아키텍처 ✅ Tier A 완료

Tier D (완료, 40개):
- [x] CPU의 구성요소 — CU/ALU/레지스터/버스
- [x] 컴퓨터 아키텍처의 종류 — 폰노이만/하버드
- [x] 기억장치의 계층구조 — 레지스터→캐시→주기억→보조기억 (tier scale)
- [x] 명령어 집합구조, CISC와 RISC
- [x] I/O제어기의 구조와 주소지정 방식의 종류 — Memory Mapped/I/O Mapped
- [x] 기억장치의 분류 및 특징 — 용도/저장방식/유지/접근/보존 5기준
- [x] 주소지정 방식 — 즉시/직접/간접/묵시/변위(상대·인덱스·베이스)
- [x] 메모리 구조에 의한 병렬 처리 시스템 분류 — SMP/MPP/NUMA
- [x] 병렬 처리 시스템의 플린에 의한 분류 — SISD/SIMD/MISD/MIMD
- [x] 저장장치 디스크 스케줄링 — FCFS/SSTF/SCAN/LOOK/C-SCAN/C-LOOK
- [x] RAID 기술 — 0/1/5/6/10
- [x] 운영체쩌별 파일시스템의 종류 — Unix/Linux/Solaris/macOS/Windows
- [x] 프로세스 관리를 위한 기법 — 생성/종료/상태전이/문맥교환
- [x] 주요 운영체제의 종류 — Windows/macOS/Android/iOS/UNIX/Linux/Windows Server
- [x] 스케줄링 알고리즘의 종류 및 특징 — FIFO/Priority/SJF/SRT/RR/Deadline/HRN/MFQ
- [x] 가상기억장치의 페이지 교체 기법 — Optimal/FIFO/LRU/LFU
- [x] 가상기억장치의 구현 기법 — 페이징/세그먼테이션
- [x] 영상압축 유형 — MPEG-1/2/4, AVC/H.264, HEVC/H.265 등
- [x] 시스템 배치 방식에 따른 시스템아키텍처 분류 — 중앙집중/지역분산
- [x] 응용 프로그램 제공 방식에 따른 분류 — 2-티어/3-티어
- [x] 하드웨어 요소별 규모 산정 방식 — CPU/메모리/디스크/스토리지
- [x] HA 구성 유형 — Hot Standby/Mutual Takeover
- [x] 클라우드 운영 형태에 따른 분류 — Public/Private/Hybrid
- [x] 서버 가상화 방식의 유형 — 전가상화/반가상화/OS레벨(컨테이너)
- [x] 클라우드 서비스 유형 — IaaS/PaaS/SaaS
- [x] Hadoop의 주요기술 요소 — HDFS/MapReduce/Hive/HBase/Sqoop/Flume/YARN
- [x] 데이터 링크계층 프로토콜 — Ethernet/Token Ring/FDDI/Wi-Fi/HDLC/PPP/Frame Relay/ATM
- [x] 데이터 링크계층 부계층 — LLC/MAC
- [x] IP 주소와 MAC 주소 변환 프로토콜 — ARP/RARP
- [x] 네트워크 계층 프로토콜 — IP/ARP/RARP/ICMP/IGMP
- [x] IPv4 주소 할당방식 — Classful/CIDR/DHCP/NAT
- [x] IPv4 표현방식 — 2진/점-10진/16진/CIDR
- [x] 라우팅 프로토콜 종류 — RIP/IGRP/OSPF/BGP
- [x] TCP 특징 — 연결지향/신뢰성/스트림/흐름·오류·혼잡 제어
- [x] UDP 특징 — 비연결/제어없음/최선형
- [x] SCTP 특징 — 다중 스트림/멀티홈잉/연결지향·신뢰성
- [x] QoS(Quality of Service) 특성 — 신뢰성/지연/지터/대역폭
- [x] 품질 구현기법 — 스케줄링/트래픽 성형·감시/자원 예약/수락 제어
- [x] VoIP 호 신호 프로토콜 — H.323/SIP/MGCP/MEGACO
- [x] RTP 주요 프로토콜 — RTP/RTCP/RTSP

### 04 정보보안 ✅ Tier A 완료 (18개)

- [x] 암호기술의 분류 — 대칭키·공개키·해시·암호 프로토콜
- [x] 비밀키 암호와 공개키 암호 알고리즘 — 블록/스트림 + RSA/ECC/DH
- [x] 인증방식의 유 — 지식/소유/존재/멀티팩터
- [x] 인증기술의 종류 — 패스워드/OTP/공인인증서/생체/FIDO
- [x] 접근통제 정책의 종류 — MAC/DAC/RBAC
- [x] 접근통제 메커니즘 — 접근통제 행렬/ACL/CL/SL
- [x] 접근통제 모델 — BLP/Biba/Clark-Wilson/Chinese Wall
- [x] 네트워크 공격의 유형과 대응 — Land/Ping of Death/Syn Flooding/Boink/DDoS/스니핑
- [x] APT 공격 — 정찰/침투/확산/유출
- [x] 통신 프로토콜 계층과 보안 — 응용(PGP·Kerberos·SSH)/전송(SSL·TLS)/인터넷(IPSec)
- [x] 양자 암호 — QKD/PQC
- [x] 데이터베이스 접근통제 정책 — DAC/MAC/RBAC 적용
- [x] 데이터베이스 암호화의 유형 — API/플러그인/TDE/하이브리드
- [x] 데이터베이스 암호화 키의 종류 — 암복호화 키/마스터 키
- [x] JAVA 시큐어 코딩 주요기법 — SQL 삽입/XSS/경로조작/자원해제/세션
- [x] C 시큐어 코딩 주요기법 — 버퍼 오버플로우/포맷 스트링/정수 오버플로우/경쟁 조건/UAF
- [x] Android-JAVA 시큐어 코딩 주요기법 — 권한/인텐트/저장 보안/네트워크/웹뷰
- [x] 시큐어 개발 생명주기 — 요구사항 정의/분석·설계/코딩/테스팅/유지보수

### 05 IT 비즈니스와 윤리 ✅ Tier A 완료 (12개)

- [x] BSC의 구성요소 — 관점/CSF/전략맵/KPI
- [x] 재무적 성과평가 기법의 종류 — ROI/NPV/IRR/PP
- [x] IT-BSC의 구성요소 — 기업공헌도/사용자/운영프로세스/미래지향
- [x] MBOS의 구성요소 — 목표설정/참여/피드백
- [x] MBO의 구성요소 — 목표설정/참여/피드백
- [x] 지식재산권의 유형 — 저작권/산업재산권/신지식재산권
- [x] 신지식재산권의 개념과 유형 — 첨단산업재산권/정보재산권/생명공학/기타
- [x] 저작권의 정의와 분류 — 저작인격권/저작재산권/저작인접권
- [x] IT 비즈니스 생태계 구성요소 — 콘텐츠/플랫폼/네트워크/디바이스/보안 (CPNDS)
- [x] 전략수립의 구성요소 — 기본정보/현재상태/미래목표/추진전략
- [x] 엔터프라이즈 솔루션의 종류 — ERP/SCM/CRM/KMS/PLM/EDW/BI
- [x] 아웃소싱의 형태 — Total/Selective/IT 자회사/Co-Sourcing

### 06 테크니컬 커뮤니케이션·PM ✅ Tier A 완료 (14개)

- [x] 비즈니스 커뮤니케이션의 요소 — 송신자/메시지/채널/수신자/피드백/정보
- [x] 비즈니스 커뮤니케이션의 유형 — 수평/하향식/상향식
- [x] 창의적 사고기법 — 브레인스토밍/6 Thinking Hats/랜덤워드/SCAMPER/TRIZ
- [x] 논리적 사고기법 — MECE/로직트리/연역법/귀납법
- [x] 합리적 의사결정 기법 — MCDM/AHP
- [x] 비즈니스 문서의 종류 — 보고서/의견서/기획서/계획서/설명서
- [x] 테크니컬 문서의 특징 — 명확성/정확성/체계성
- [x] 테크니컬 문서의 종류 — 프로젝트관리/요구사항·설계/개발/테스트/사용자 문서
- [x] 프로젝트 조직구조 — 기능/약한·균형·강한 매트릭스/프로젝트 중심 (tier scale)
- [x] 작업분류체계(WBS) — 작업패키지/식별번호/WBS 사전/RAM
- [x] 일정개발 기법-임계경로기법(CPM) — 전진계산/후진계산/ES·EF·LS·여유시간
- [x] 일정개발 기법-주공정연쇄기법(CCM) — 프로젝트/공급/자원 완충
- [x] 일정단축 기법 — 공정압축법(Crashing)/공정중첩단축법(Fast Tracking)
- [x] 프로젝트 평가단계와 주안점 — 사전/중간/사후

---

## 10. 통계

| 과목 | Tier A 미완 | Tier B 미완 | 완료 | 합계 |
|---|---:|---:|---:|---:|
| 01 소프트웨어 개발 | 0 | 0 | 18 | 18 |
| 02 데이터 | 0 | 0 | 28 | 28 |
| 03 시스템 아키텍처 | 0 | 0 | 40 | 40 |
| 04 정보보안 | 0 | 0 | 18 | 18 |
| 05 IT 비즈니스 | 0 | 0 | 12 | 12 |
| 06 커뮤니케이션·PM | 0 | 0 | 14 | 14 |
| **합계** | **0** | **0** | **130** | **130** |

**🎉🎉 전체 완료 — Tier A(125) + Tier B(5) = 130개 enrichment 완료.**

통계는 §9 체크박스 기준으로 갱신.

## 11. 참고: 기 완료 예시 (패턴)

- **enrichment 스크립트 템플릿:** `enrich_응집결합.py`
- **실제 생성 결과:** `topcit_lesson/01/index.html` → "응집도" 또는 "결합도" 카드 클릭
- **렌더 구현:** `gen_topcit.py` 내 `renderTypesSection()` 함수

## 12. 문서 업데이트 규칙

- Enrichment 완료 시 §9에서 해당 항목을 `[ ]` → `[x]`로.
- 건너뛴(원본 불분명) 항목은 `[~]`와 짧은 사유 메모.
- §10 통계는 체크박스 기준 재계산.
- 새 Tier 재분류가 필요하면 §9 해당 과목 섹션에 추가.
- 진행 중단 시 마지막 커밋 해시나 날짜를 하단에 메모해두면 다음 세션이 안전하게 이어받음.
