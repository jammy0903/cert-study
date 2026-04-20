"""
TOPCIT OCR 텍스트 → 구조화 JSON 변환기 (개선판)
- TOC 중복 제거
- OCR 오류 보정
- 가짜 섹션 필터링
- 세부항목 구조 정교화
"""
import re
import json
import os

SUBJECTS = {
    '01': '소프트웨어 개발',
    '02': '데이터 이해와 활용',
    '03': '시스템 아키텍처 이해와 활용',
    '04': '정보보안 이해와 활용',
    '05': 'IT 비즈니스와 윤리',
    '06': '테크니컬 커뮤니케이션과 프로젝트 관리',
}

KO = r'[\uAC00-\uD7A3]'

# ── OCR 오류 보정 사전 ────────────────────────────────────
OCR_FIXES = [
    # 괄호 안 순수 숫자/잡음 제거 (예: (10101788017 Hiding) → (Information Hiding) 불가하므로 제거)
    (re.compile(r'\(\d{4,}[^\)]*\)'), ''),
    (re.compile(r'\([\dA-Za-z/\\\[\]{}|@#$%^&*+=<>]{6,}\)'), ''),
    # 숫자만 남은 잡음 제거
    (re.compile(r'\s+\d{1,3}\s*$'), ''),
    # 흔한 OCR 오류 보정
    (re.compile(r'동양(?=\s|$)'), '동향'),
    (re.compile(r'오른소스|오프소스'), '오픈소스'),
    (re.compile(r'개발모구'), '개발도구'),
    (re.compile(r'주상화'), '추상화'),
    (re.compile(r'BYE\s*=?[-—]+\s*XP'), '방법론 XP'),
    (re.compile(r'XHAKS'), '재사용'),
    (re.compile(r'FAs\s*$'), '조직 유형'),
    (re.compile(r'HHA\]?X'), '프로시저'),
    (re.compile(r'0Y2!'), '매핑'),
    (re.compile(r'Set\s*$'), '동향'),
    (re.compile(r'03\[3\s*Structure'), 'Data Structure'),
    (re.compile(r'10ㅁ\d*'), 'IDE'),
    (re.compile(r'466\s*Interface'), 'User Interface'),
    (re.compile(r'2464\s*\(?User Experience\)?'), '경험(User Experience)'),
    (re.compile(r'언어\s+님\s*$'), '언어 개념'),
    (re.compile(r'ee\s+(목적|정의|유형)'), r'\1'),
    (re.compile(r'도델'), '모델'),
    (re.compile(r'재시\s*$'), '재사용의 대상'),
    (re.compile(r'유지보수\s*절\s*$'), '유지보수 절차'),
    (re.compile(r'기술\s+동\s*$'), '기술 동향'),
    (re.compile(r'개발\s+동\s*$'), '개발 동향'),
    (re.compile(r'4174\(Transaction'), '설계(Transaction'),
    (re.compile(r'065190\s*Pattern'), 'Design Pattern'),
    (re.compile(r'BE\(UX\)Zt'), '경험(UX)과'),
    (re.compile(r'\\\!'), 'UI'),
    (re.compile(r'OfO\|C\|HS|OfO\|C\|HZ'), '아이디어를'),
    (re.compile(r'0760<'), 'Check'),
    (re.compile(r'\d{2,}<'), ''),
    (re.compile(r'스크럼\(\d+\)'), '스크럼(Scrum)'),
    (re.compile(r'코드스멜\([^)]+\)'), '코드스멜(Code Smell)'),
    (re.compile(r'60004816[^\)]*\)'), 'Software Configuration Management)'),
    (re.compile(r'West|Best(?=\s)'), '프로토콜'),
    (re.compile(r'우픈소스'), '오픈소스'),
    (re.compile(r'->@:\s*\d*'), ''),
    (re.compile(r'¥!='), '빌드'),
    (re.compile(r'\(25\)\s*(개념)'), r'(IDE) \1'),
    (re.compile(r'\(과\s*사용자'), '(UX)과 사용자'),
    (re.compile(r'인터페이스\(\)'), '인터페이스(UI)'),
    (re.compile(r'형상관리2\|\s*정의'), '형상관리의 정의'),
    (re.compile(r'저장소\(30\)'), '저장소(Git)'),
    (re.compile(r'소프트웨어\s+목적\s*$'), '소프트웨어 유지보수의 목적'),
    (re.compile(r'HBA\s*모델'), '컨텍스트(Context) 모델'),
    # 고빈도 OCR 오류: "의" → "2|" 또는 "Z|" 또는 "2] "
    (re.compile(r'2\|\s*'), '의 '),
    (re.compile(r'Z\|\s*'), '의 '),
    (re.compile(r'2\]\s*'), '의 '),
    (re.compile(r'39\]\s*'), '의 '),
    # XML 관련 잡음
    (re.compile(r'[×Ｘ][\\\/\/][ＬL]'), 'XML'),
    (re.compile(r'XLL\b'), 'XSL'),
    (re.compile(r'×%\/Ｌ'), 'XML'),
    # 대괄호 → 소괄호 보정 (숫자 뒤)
    (re.compile(r'\[(\d+)[/\\\|]'), r'(\1)'),
    # 분석/DB 관련 오류
    (re.compile(r'OLAPS!'), 'OLAP의'),
    (re.compile(r'40601\.의'), 'NoSQL의'),
    (re.compile(r'NoSQL2\|\s*'), 'NoSQL의 '),
    (re.compile(r'SQLO\|\s*'), 'SQL의 '),
    (re.compile(r'SQL3[9\d]\]\s*'), 'SQL의 '),
    (re.compile(r'60Ｌ_'), 'SQL'),
    (re.compile(r'60\s+'), 'SQL '),
    (re.compile(r'aE\s+HEH'), '교착상태(Deadlock)'),
    (re.compile(r'S&'), '중복성'),
    (re.compile(r'BR\s*$'), '유형'),
    (re.compile(r'뷰를\s+se\s+'), '뷰를 통한 '),
    # 네트워크 관련
    (re.compile(r'\[2\/600180061\s*Protocol\s*Version\s*6\)'), 'IPv6('),
    (re.compile(r'Pv62\|\s*'), 'IPv6의 '),
    (re.compile(r'IPV62\|\s*'), 'IPv6의 '),
    (re.compile(r'MACZA\s*'), 'MAC 주소 '),
    (re.compile(r'VoP\s*S\('), 'VoIP 호('),
    (re.compile(r'VolP\b'), 'VoIP'),
    (re.compile(r'SCIP\s*프로토콜'), 'SCTP 프로토콜'),
    # 하둡 관련
    (re.compile(r'SHE\b'), 'Hadoop'),
    (re.compile(r'Sk=\b'), 'Hadoop'),
    # 고가용성/재난복구 관련
    (re.compile(r'\(3\s+tolerant'), '(Fault tolerant'),
    (re.compile(r'\(가3,'), '(DRS,'),
    # 인공지능 관련
    (re.compile(r'인공지능의\s+핀'), '인공지능의 발전'),
    (re.compile(r'빅데이터\s+시스템의\s*$'), '빅데이터 시스템의 동향'),
    # 트랜잭션 관련
    (re.compile(r'반복\s+읽\s*[^\s]+'), '반복 읽기(Repeatable Read)'),
    (re.compile(r'격리수준\(\d+\.\d+\s*Level\)'), '격리수준(Isolation Level)'),
    (re.compile(r'데이터복구\s*'), '데이터 복구의 '),
    (re.compile(r'복구조치'), '복구 조치'),
    # Hadoop 추가 패턴 (한글 뒤에도 처리)
    (re.compile(r'\bSHE(?=의|을|를|이|가|\s|$)'), 'Hadoop'),
    (re.compile(r'\bSHS(?=의|을|를|이|가|\s|$)'), 'Hadoop'),
    (re.compile(r'\bSH\b(?!\s*보안|\s*제공|\s*특성|\s*서비스|\s*시스템|\s*인증)'), 'Hadoop'),
    (re.compile(r'Sk=\s*'), 'Hadoop '),
    (re.compile(r'SHS의'), 'Hadoop의'),
    # XML 추가 패턴
    (re.compile(r'[×Ｘ]\\\/Ｌ'), 'XML'),
    (re.compile(r'XSL\s+개념\s+및\s*$'), 'XSL 개념 및 특징'),
    (re.compile(r'NoSQL의\s+저장방\s*$'), 'NoSQL의 저장방식'),
    (re.compile(r'라\)\s+기계\s*$'), '라) 기계학습(Machine Learning)'),
    (re.compile(r'^기계\s*$'), '기계학습(Machine Learning)'),
    (re.compile(r'인터넷\s+전화.*다이0001란\?'), 'VoIP(Voice over Internet Protocol)란?'),
    (re.compile(r'다이0001란\?'), 'Protocol)란?'),
    (re.compile(r'링크계층\s+Best'), '링크계층 프로토콜'),
    (re.compile(r'나\)\s+히\s*$'), '나) 하이퍼바이저(Hypervisor)'),
    (re.compile(r'다\)\s+01\s+주요기술'), '다) RTP 주요기술'),
    (re.compile(r'나\)\s+인증방식의\s+유\s*$'), '나) 인증방식의 유형'),
    (re.compile(r'라\)\s+모바일\s+보\s*$'), '라) 모바일 보안'),
    (re.compile(r'최신\s+정보기술\s+관련\s+보안동\s*$'), '최신 정보기술 관련 보안동향'),
    (re.compile(r'\(19\s+Management\)'), '(Risk Management)'),
    (re.compile(r'규모\s+산\s+산정'), '규모 산정'),
    (re.compile(r'나\)\s+Pv6의\s+등장'), '나) IPv6의 등장'),
    (re.compile(r'\(Internet\s+Protocol\s+Version\s+6\)\s+주소란\?'), 'IPv6(Internet Protocol Version 6) 주소란?'),
    (re.compile(r'IIPv4'), 'IPv4'),
    (re.compile(r'나\)\s+빅데이터\s+시스템의\s+동향\s*$'), '나) 빅데이터 시스템의 전망'),
    (re.compile(r'클라우드\s+oT\b'), '클라우드 IoT'),
    (re.compile(r'\boT\s+0\s+TO\b'), 'IoT'),
    # 최종 잔여 이슈
    (re.compile(r'IPV6'), 'IPv6'),
    (re.compile(r'IPV4'), 'IPv4'),
    (re.compile(r'ITIL\d+'), 'ITIL'),
    (re.compile(r'가\)\s+866의'), '가) BSC의'),
    (re.compile(r'\bㅣ\s+비즈니스'), 'IT 비즈니스'),
    (re.compile(r'\bㅣ\s+거버넌스'), 'IT 거버넌스'),
    (re.compile(r'\/036:'), 'WBS:'),
    (re.compile(r'\[ㅁ\s*,?'), '(FP,'),
    (re.compile(r'기능점수법\(『+,'), '기능점수법(FP,'),
    (re.compile(r'\s+Ge\s+'), ' '),
    (re.compile(r'—-Phase'), '--Phase'),
    (re.compile(r'Flow\s+—Oriented'), 'Flow-Oriented'),
    (re.compile(r'View—Controller'), 'View-Controller'),
    # IPv4/IPv6 추가 패턴
    (re.compile(r'\bPv6(?=의|를|가|\s|$)'), 'IPv6'),
    (re.compile(r'\bPv4(?=의|를|가|\s|$)'), 'IPv4'),
    (re.compile(r'\bPv6\b'), 'IPv6'),
    (re.compile(r'\bPv4\b'), 'IPv4'),
    (re.compile(r'\|PvA\b'), 'IPv4'),
    (re.compile(r'IPv6Q\|\s*'), 'IPv6의 '),
    (re.compile(r'IPv6의\s+sme'), 'IPv6의 특징'),
    (re.compile(r'\(2\)600180061\s*Protocol\s*Version\s*6\)'), '(Internet Protocol Version 6)'),
    (re.compile(r'Pv4\s+FAS\s+사용한'), 'IPv4를 사용한'),
    (re.compile(r'네트워크\(예\)'), '네트워크 구성(예)'),
    # CPU/명령어 관련
    (re.compile(r'명령어\s+A\}O\|Z'), '명령어 사이클'),
    (re.compile(r'CISC\}\s*RISC'), 'CISC와 RISC'),
    (re.compile(r'\|/0'), 'I/O'),
    # 보안 관련
    (re.compile(r'파밍\(마\d+\)'), '파밍(Pharming)'),
    (re.compile(r"Ge\s*\"Fileless\""), '및 "Fileless"'),
    (re.compile(r'이상금융거래\s+탐지시스템\(\d+:'), '이상금융거래 탐지시스템(FDS:'),
    (re.compile(r'2\'B\s*\d?\s*개념'), '인증(Authentication) 개념'),
    (re.compile(r'암호화\s+키\s*\|\s*\(Key\)'), '암호화 키(Key)'),
    # IT비즈니스 관련
    (re.compile(r'\boT\s+0\s+TO\b'), 'IoT'),
    (re.compile(r'클라우드\s+oT\s+'), '클라우드 IoT '),
    (re.compile(r'ERPS?\|\s*'), 'ERP의 '),
    (re.compile(r'ERPS?\s+이해'), 'ERP의 이해'),
    (re.compile(r'501\/의'), 'SCM의'),
    (re.compile(r'PLM\]\s*이해'), 'PLM의 이해'),
    (re.compile(r'SLAQ\|\s*'), 'SLA의 '),
    (re.compile(r'MEBE\|\s*'), 'MBO의 '),
    (re.compile(r'\b866\b'), 'BSC'),
    (re.compile(r'IT-BSC의\s+개요'), 'IT-BSC의 개요'),
    (re.compile(r'TS\]\s*전사적'), '의 전사적'),
    (re.compile(r'\b1\s+거버넌스\b'), 'IT 거버넌스'),
    (re.compile(r'\bㅣ\s+거버넌스\b'), 'IT 거버넌스'),
    (re.compile(r'\bㅣ\s+비즈니\b'), 'IT 비즈니스'),
    (re.compile(r'비즈니스와\s+11의'), '비즈니스와 IT의'),
    (re.compile(r'HWSAL\s+IT'), 'H/W 및 IT'),
    (re.compile(r'H\/W2SA\!\s+IT'), 'H/W 및 IT'),
    (re.compile(r'107\s+기술'), 'ICT 기술'),
    # 프로젝트관리
    (re.compile(r'전담조직\(040\)'), '전담조직(PMO)'),
    (re.compile(r'작업분류체계\(//\d+:'), '작업분류체계(WBS:'),
    (re.compile(r'프로젝트관리\s+영\s*$'), '프로젝트관리 영역'),
    (re.compile(r'문서\s+작송'), '문서 작성'),
    (re.compile(r'비즈니\s+라\s*$'), '비즈니스 인프라'),
    # 잘린 문장들
    (re.compile(r'아웃\.\s*$'), '아웃소싱의 효과'),
    (re.compile(r'미의\s+이해'), 'BI의 이해'),
    (re.compile(r'임베디드\s+소프\s*$'), '임베디드 소프트웨어'),
    (re.compile(r'임베디드\s+소프트웨어의\s*$'), '임베디드 소프트웨어의 정의'),
    (re.compile(r'빅데이터\s+시스템의\s*$'), '빅데이터 시스템의 현황'),
    (re.compile(r'오픈소스\s+소프\s*$'), '오픈소스 소프트웨어'),
    (re.compile(r'가\)\s+언어\s*$'), '가) C 언어'),
    (re.compile(r'동적\s+SQLat\s+정적'), '동적 SQL과 정적'),
    (re.compile(r'SQLe\|\s*코드\s+예'), 'SQL의 코드 예'),
    (re.compile(r'다\)\s+01\s+주요기술'), '다) RTP 주요기술'),
    (re.compile(r'클라우드\s+AEH'), '클라우드 서비스 유형'),
    (re.compile(r'나\)\s+히\s*$'), '나) 하이퍼바이저'),
    (re.compile(r'종:\s*$'), '종류'),
    (re.compile(r'HWSA의'), 'H/W 소프트웨어의'),
    (re.compile(r'BYES\s+위한'), '작성을 위한'),
    # 기타
    (re.compile(r'데이터베이스\(00:'), '데이터웨어하우스(DW:'),
    (re.compile(r'임베디드\[67060060\)'), '임베디드'),
    (re.compile(r'Repedtale\s*\|\s*Read'), 'Repeatable Read'),
    (re.compile(r'630\s+Uncommitted'), 'Read Uncommitted'),
    (re.compile(r'8630\s+Committed'), 'Read Committed'),
    (re.compile(r'객체관계\s+데이터베이스\(아028\)'), '객체관계 데이터베이스(ORDB)'),
    (re.compile(r'엔터티\[?5008\]?/?'), '엔터티(Entity)'),
    (re.compile(r'속성\(새07046\)'), '속성(Attribute)'),
    (re.compile(r'일반화\/특수화\([\(\ㅎ\d해]+\/\d+\)'), '일반화/특수화(Generalization/Specialization)'),
    (re.compile(r'08\s+설계'), 'DB 설계'),
    # 남은 OCR 오류들
    (re.compile(r'OH2!'), '매핑'),
    (re.compile(r'Z74\\?\(Relational'), '관계(Relational'),
    (re.compile(r'=의\s+변\s*$'), '의 변환'),
    (re.compile(r'z\}\s*정적'), '와 정적'),
    (re.compile(r'SQLz\}'), 'SQL과'),
    (re.compile(r'60\s+의'), 'SQL의'),
    (re.compile(r'60_의'), 'SQL의'),
    (re.compile(r'60\s+과'), 'SQL과'),
    (re.compile(r'60e\|'), 'SQL의'),
    (re.compile(r'[×Ｘ][\\\/][ＬL]의'), 'XML의'),
    (re.compile(r'[×Ｘ]%\/Ｌ'), 'XML'),
    (re.compile(r'데이터베이스\s+시스템\(088,\s*Database\s*8%9187\/'),'데이터베이스 시스템(DBS, Database System)'),
    (re.compile(r'\(088,'), '(DBS,'),
    (re.compile(r'8%9187\//?\)'), 'System)'),
    (re.compile(r'데이터아키텍트\(24\)'), '데이터아키텍트(DA)'),
    (re.compile(r'관리자\(284'), '관리자(DBA'),
    (re.compile(r'24\/의'), 'DA)의'),
    (re.compile(r'메인\s+메모리\s+데이터베이스\(408\)'), '메인 메모리 데이터베이스(MMDB)'),
    (re.compile(r'\(160\.3400\s*Level\)'), '(Isolation Level)'),
    (re.compile(r'데이터마이닝의\s+개념\s+및\s+알고리\s*$'), '데이터마이닝의 개념 및 알고리즘'),
    (re.compile(r'알고리\s*$'), '알고리즘'),
    (re.compile(r'정규화를\s+적\s*$'), '정규화를 적용한 데이터베이스 설계'),
    (re.compile(r'\[001:'), '(DCL:'),
    (re.compile(r'조작어\(1:'), '조작어(DML:'),
    (re.compile(r'S\(Call\)'), '호(Call)'),
    (re.compile(r'101\s+개념'), 'RTP 개념'),
    (re.compile(r'101\s+표준'), 'RTP 표준'),
    (re.compile(r'101\s+주요'), 'RTP 주요'),
    (re.compile(r'\(가3,'), '(DRS,'),
    (re.compile(r'ots\s+7\s*ltt'), '기타'),
    (re.compile(r'SE\|0\+0\|'), '옵티마이저(Optimizer)'),
    (re.compile(r'OLAP의\s*!\s*개념'), 'OLAP의 개념'),
    (re.compile(r'빅데이터의\s+Life\s+Cycle'), '빅데이터의 Life Cycle'),
    # 이중 의 제거 및 잔여 파이프 기호 정리
    (re.compile(r'의\s+의\s+'), '의 '),
    (re.compile(r'(\w)\|\s*이해'), r'\1의 이해'),
    (re.compile(r'(\w)\|\s*개요'), r'\1의 개요'),
    (re.compile(r'(\w)\|\s*구성요소'), r'\1의 구성요소'),
    (re.compile(r'(\w)\|\s*구성'), r'\1의 구성'),
    (re.compile(r'(\w)\|\s*특징'), r'\1의 특징'),
    (re.compile(r'(\w)\|\s*종류'), r'\1의 종류'),
    (re.compile(r'(\w)\|\s*정의'), r'\1의 정의'),
    (re.compile(r'(\w)\|\s*역할'), r'\1의 역할'),
    (re.compile(r'(\w)\|\s*관리'), r'\1의 관리'),
    (re.compile(r'(\w)\|\s*활용'), r'\1의 활용'),
    (re.compile(r'(\w)9\|\s*'), r'\1의 '),
    # DB/SQL 관련
    (re.compile(r'68\s+표기법'), 'ER 표기법'),
    (re.compile(r'엔터티6705/\)'), '엔터티(Entity)'),
    (re.compile(r'키<60\)'), '키(Key)'),
    (re.compile(r'\(00:\s*Data\s+Warehouse\)'), '(DW: Data Warehouse)'),
    (re.compile(r'\(00:\s*Data\s+Definition'), '(DDL: Data Definition'),
    (re.compile(r'\(001:\s*Data\s+Control'), '(DCL: Data Control'),
    (re.compile(r'033\s+Mining'), 'Data Mining'),
    (re.compile(r'\|\s+Read\)\s*$'), ')'),
    # CPU/OS 관련
    (re.compile(r'\(14,\s*High\s*Availability'), '(HA, High Availability'),
    (re.compile(r'고가용성,\s*High'), '고가용성(HA, High'),
    (re.compile(r'\(25,\s*Operating\s*System'), '(OS, Operating System'),
    (re.compile(r'운영체제\(25\)'), '운영체제(OS)'),
    (re.compile(r'\(ㅇ004,\s*Central\s*Processing\s*Unit'), '(CPU, Central Processing Unit'),
    (re.compile(r'CPUS\]\s*정의'), 'CPU의 정의'),
    (re.compile(r'CPUS\]\s*수행'), 'CPU의 수행'),
    (re.compile(r'CPUS\]\s*구성'), 'CPU의 구성'),
    (re.compile(r'스레드\(680\)'), '스레드(Thread)'),
    (re.compile(r'\(03\(31\.6\.\s*Processing\s*System\)'), '(Parallel Processing System)'),
    (re.compile(r'파일\s+tie!\s*이해'), '파일시스템의 이해'),
    (re.compile(r'ZEMIA'), '프로세스'),
    (re.compile(r'SUHA\(UNIX\)'), 'UNIX'),
    # Hadoop 관련
    (re.compile(r'\bSH[ES]?\b(?!\s*보안)'), 'Hadoop'),
    (re.compile(r'SKS\s+지원'), 'Hadoop 지원'),
    # 네트워크 관련
    (re.compile(r'논리\s+링크\s+제어\(0\)'), '논리 링크 제어(LLC)'),
    (re.compile(r'매체\s+접근\s+제어0/&0\)'), '매체 접근 제어(MAC)'),
    (re.compile(r'데이터\s+GAAS\s*SI'), '데이터 링크계층'),
    (re.compile(r'링크계층\s+Yast'), '링크계층 프로토콜'),
    (re.compile(r'계층\s+Bast'), '계층 프로토콜'),
    (re.compile(r'계층\s+Sst'), '계층 프로토콜'),
    (re.compile(r'인터넷\s+전화\s+개념.*다이0001란\?'), 'VoIP란?'),
    (re.compile(r'호\(081\s+신호'), '호 신호'),
    (re.compile(r'인터넷\s+표\s*$'), '인터넷 표준'),
    # 보안 관련
    (re.compile(r'점근제어'), '접근제어'),
    (re.compile(r'\(3\\\/6\)'), '(ISMS)'),
    (re.compile(r'부인방지\([^\)]{5,}\)'), '부인방지(Non-Repudiation)'),
    (re.compile(r'암호화와\s+\$5\s*Decryption\)'), '암호화와 복호화(Decryption)'),
    (re.compile(r'관리체계!?\d*[-ㅁ]+\)'), '관리체계(ISMS-P)'),
    (re.compile(r'시큐어\s+코딩\s+주요7'), '시큐어 코딩 주요기법'),
    (re.compile(r'C\s+시큐어\s+코딩\s+주요7'), 'C 시큐어 코딩 주요기법'),
    (re.compile(r'loT\s+보안'), 'IoT 보안'),
    # BSC/MBO 관련
    (re.compile(r'\b866\b'), 'BSC'),
    (re.compile(r'MBOS\s+기업'), 'MBO를 기업'),
    (re.compile(r'MBOS\|\s*'), 'MBO의 '),
    (re.compile(r'MBOS\s+'), 'MBO를 '),
    # 문서작성 관련
    (re.compile(r'작송\s*$'), '작성'),
    (re.compile(r'문서\s+작\s*$'), '문서 작성'),
    (re.compile(r'테크니컬\s+문서\s*작\s*$'), '테크니컬 문서 작성'),
    (re.compile(r'테크ㄴ'), '테크니컬'),
    (re.compile(r'\(1:\s*Request\s*For\s*Information\)'), '(RFI: Request For Information)'),
    (re.compile(r'\(가:\s*Request\s*For\s*Proposal\)'), '(RFP: Request For Proposal)'),
    (re.compile(r'BYES\s+위한'), '작성을 위한'),
    (re.compile(r'문저해결'), '문제해결'),
    # IT비즈니스 관련
    (re.compile(r'60/1[『「]?SQL\s+12207'), 'ISO/IEC 12207'),
    (re.compile(r'\bWe\s+IT'), 'Web IT'),
    (re.compile(r'9\\중심'), 'AI 중심'),
    (re.compile(r'프로젝트관리\s+도구\(다이\s*![\d\w]+\[?\s*System,'), '프로젝트관리 도구(Project Management System,'),
    (re.compile(r'60씨과\s*NFV'), 'SDN과 NFV'),
    (re.compile(r'교가용성'), '고가용성'),
    (re.compile(r'\s{2,}'), ' '),
]

def fix_ocr(text: str) -> str:
    for pat, repl in OCR_FIXES:
        text = pat.sub(repl, text)
    return text.strip()

# ── 패턴 ─────────────────────────────────────────────────
RE_CHAPTER = re.compile(
    r'^[\|IiⅠ]{1,4}[VvⅤ]?[IiⅠ]{0,3}[.,。]\s*(' + KO + r'.{2,40})$'
)
RE_SECTION = re.compile(r'^(\d{2})\s+(' + KO + r'[^\n]{3,50})$')
RE_SUB = re.compile(r'^([가-힣])\)\s*(.{2,60})$')
RE_BULLET = re.compile(r'^[ㆍ・•]\s*(.+)$')
RE_QUIZ_MARKER = re.compile(
    r'(정의|개념|목적|특징|장점|단점|종류|유형|비교|절차|단계|원칙|구성요소|차이점|역할|효과|방법|기법|원리)'
)
RE_PAGE_FOOTER = re.compile(
    r'^(ESSENCE|TOPCIT|CONTENTS|\d+\s+(TOPCIT|ESSENCE)|기술영역|\d+$|Mi?\s)'
)
# TOC 구간 감지: "NN 제목 ....... NNN" 패턴 (목차 특유의 점선+페이지번호)
RE_TOC_LINE = re.compile(r'' + KO + r'.{3,}\.{3,}\s*\d+$')

def is_noise(s: str) -> bool:
    if not s or len(s) < 2:
        return True
    if RE_PAGE_FOOTER.match(s):
        return True
    ko = len(re.findall(KO, s))
    if ko <= 1 and not re.search(r'[A-Za-z]{3,}', s):
        return True
    if re.match(r'^[\d\W\s]+$', s):
        return True
    return False

def is_fake_section(title: str) -> bool:
    """가짜 섹션 판별"""
    ko = len(re.findall(KO, title))
    if ko < 4:
        return True
    # 동사/조사로 끝나는 긴 문장 → 본문
    if len(title) > 40 and re.search(r'(있다|된다|한다|이다|것이|위해|통해|하여|이며|으로)\s*$', title):
        return True
    # 괄호+숫자로 시작하는 잔재
    if re.match(r'^[\(\[]\s*\d', title):
        return True
    # OCR 잡음 비율 높음 (ASCII 특수문자 3개 이상)
    noise = len(re.findall(r'[^\w\s\uAC00-\uD7A3\u4E00-\u9FFF\(\)\-]', title))
    if noise >= 3:
        return True
    return False

def is_fake_sub(title: str) -> bool:
    """가짜 세부항목 판별"""
    # 마커가 가/나/다/라/마/바/사/아 가 아닌 것 (등, 개 등 OCR 오류)
    # → RE_SUB에서 이미 가-힣으로 제한하나, 등/개/개 같은 비표준 마커 필터
    ko = len(re.findall(KO, title))
    if ko < 1:
        return True
    # 긴 본문 문장
    if len(title) > 50:
        return True
    # OCR 잡음 비율
    noise = len(re.findall(r'[^\w\s\uAC00-\uD7A3\(\)\-\.]', title))
    if noise >= 4:
        return True
    return False

RE_CHAPTER_START = re.compile(r'^(I{1,4}V?I{0,3}|\|{1,4})[.,。]\s*' + KO)
RE_SECTION_CONTENT = re.compile(r'^0[1-4]\s+' + KO + r'.{5,}')  # 내용이 충분한 섹션

def find_content_start(lines: list[str]) -> int:
    """TOC 끝나고 실제 내용 시작하는 라인 인덱스 반환"""
    total = len(lines)

    # 전략 1: 점선+페이지번호 패턴 (TOC with dots)
    toc_end = 0
    for i, line in enumerate(lines):
        if RE_TOC_LINE.search(line.strip()):
            toc_end = i
    if toc_end >= 50:
        return toc_end + 30

    # 전략 2: CONTENTS 섹션 이후 일정 줄 스킵
    for i, line in enumerate(lines):
        if 'CONTENTS' in line and i > 10:
            # CONTENTS 이후 200줄 내에서 실제 챕터 시작 찾기
            for j in range(i + 1, min(i + 300, total)):
                s = lines[j].strip()
                if RE_CHAPTER_START.match(s):
                    return j
            return i + 100

    # 전략 3: 파일 앞 12%는 표지/목차로 간주
    skip = max(50, total // 8)
    # 단, 스킵 구간 이후 첫 챕터 헤더 찾기
    for i in range(skip, min(skip + 200, total)):
        s = lines[i].strip()
        if RE_CHAPTER_START.match(s) or (RE_SECTION_CONTENT.match(s) and i > skip + 30):
            return i

    return skip

def extract_keywords(lines: list[str]) -> list[str]:
    kws = set()
    for line in lines:
        s = line.strip()
        # "한국어 용어(English Term)" 패턴
        for m in re.finditer(r'(' + KO + r'{2,10})\s*[\(\[（]([A-Za-z][A-Za-z\s]{2,25})[\)\]）]', s):
            kws.add(m.group(1))
        # "X라 한다 / X를 의미" 패턴
        for m in re.finditer(r'(' + KO + r'{2,12})(?:라고|이라|란|을|를)\s*(?:한다|정의|의미|말한다)', s):
            kws.add(m.group(1))
        # 불릿 첫 어절
        bm = RE_BULLET.match(s)
        if bm:
            fw = bm.group(1).split()
            if fw and re.search(KO + '{2,}', fw[0]):
                kws.add(fw[0])
    return [k for k in list(kws) if len(k) >= 2][:12]

def extract_quiz_points(subsections: list[dict]) -> list[str]:
    points = []
    for sub in subsections:
        title = sub.get('title', '')
        if RE_QUIZ_MARKER.search(title):
            points.append(f"{sub.get('marker','')} {title}")
        if len(sub.get('bullets', [])) >= 3:
            points.append(f"{sub.get('marker','')} {title} [열거형]")
    return points

def dedup_sections(sections: list[dict]) -> list[dict]:
    """제목 기준으로 중복 섹션 제거 — 세부항목이 더 많은 것을 유지"""
    seen: dict[str, int] = {}
    result = []
    for sec in sections:
        key = sec['title'].strip()
        if key in seen:
            prev = result[seen[key]]
            # 현재가 더 풍부하면 교체
            if len(sec['subsections']) > len(prev['subsections']):
                result[seen[key]] = sec
        else:
            seen[key] = len(result)
            result.append(sec)
    return result

def parse_file(filepath: str, subject_id: str) -> dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()

    # TOC 이후부터만 파싱
    content_start = find_content_start([l.rstrip() for l in raw_lines])

    subject = {
        'id': subject_id,
        'title': SUBJECTS.get(subject_id, ''),
        'chapters': [],
        'sections': []
    }

    current_chapter = None
    current_section = None
    current_sub = None
    sec_local_lines: list[list[str]] = []

    def new_chapter(title):
        nonlocal current_chapter, current_section, current_sub
        current_chapter = {'title': title, 'section_refs': []}
        current_section = None
        current_sub = None
        subject['chapters'].append(current_chapter)

    def new_section(num, title):
        nonlocal current_section, current_sub
        title = fix_ocr(title)
        if is_fake_section(title):
            return False
        sec = {
            'num': num,
            'title': title,
            'chapter': current_chapter['title'] if current_chapter else '',
            'keywords': [],
            'subsections': [],
            'quiz_points': []
        }
        current_section = sec
        current_sub = None
        subject['sections'].append(sec)
        sec_local_lines.append([])
        if current_chapter:
            current_chapter['section_refs'].append(num)
        return True

    def new_sub(marker, title):
        nonlocal current_sub
        title = fix_ocr(title)
        if not title or is_fake_sub(title):
            return
        # 비표준 마커(등, 개 등) 필터 — 가~자 사이만 허용
        if marker not in '가나다라마바사아자차카타파하':
            return
        sub = {'marker': marker + ')', 'title': title, 'content': '', 'bullets': []}
        current_sub = sub
        if current_section:
            current_section['subsections'].append(sub)

    for raw_line in raw_lines[content_start:]:
        line = raw_line.rstrip('\n')
        s = line.strip()

        if is_noise(s) or RE_TOC_LINE.search(s):
            continue

        m_sec = RE_SECTION.match(s)
        m_sub = RE_SUB.match(s)
        m_ch = RE_CHAPTER.match(s)
        m_bullet = RE_BULLET.match(s)

        if m_sec and 1 <= int(m_sec.group(1)) <= 10:
            new_section(m_sec.group(1), m_sec.group(2).strip())
        elif m_ch and not m_sec:
            new_chapter(fix_ocr(m_ch.group(1)))
        elif m_sub:
            new_sub(m_sub.group(1), m_sub.group(2).strip())

        if current_section and sec_local_lines:
            sec_local_lines[-1].append(s)
            if m_bullet and current_sub:
                current_sub['bullets'].append(fix_ocr(m_bullet.group(1)))
            elif not m_sec and not m_sub and not m_ch and current_sub:
                cleaned = fix_ocr(s)
                if cleaned:
                    current_sub['content'] = (current_sub['content'] + ' ' + cleaned).strip()

    # 중복 섹션 제거
    subject['sections'] = dedup_sections(subject['sections'])

    # 키워드 & 퀴즈포인트 후처리
    for i, sec in enumerate(subject['sections']):
        lines = sec_local_lines[i] if i < len(sec_local_lines) else []
        sec['keywords'] = extract_keywords(lines)
        sec['quiz_points'] = extract_quiz_points(sec['subsections'])
        for sub in sec['subsections']:
            sub['content'] = sub['content'][:400]

    return subject


def main():
    import sys
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(SUBJECTS.keys())
    out_dir = '/home/jammy/projects/cert-study/topcit_json'
    os.makedirs(out_dir, exist_ok=True)

    for num in targets:
        in_path = f'/home/jammy/projects/cert-study/topcit_texts/topcit_{num}.txt'
        out_path = f'{out_dir}/topcit_{num}.json'
        if not os.path.exists(in_path):
            print(f'[{num}] 파일 없음')
            continue

        print(f'[{num}] {SUBJECTS[num]} 파싱 중...')
        data = parse_file(in_path, num)

        sec_cnt = len(data['sections'])
        sub_cnt = sum(len(s['subsections']) for s in data['sections'])
        qp_cnt = sum(len(s['quiz_points']) for s in data['sections'])
        kw_cnt = sum(len(s['keywords']) for s in data['sections'])

        print(f'  → 챕터 {len(data["chapters"])}개 | 소단원 {sec_cnt}개 | 세부항목 {sub_cnt}개 | 키워드 {kw_cnt}개 | 퀴즈포인트 {qp_cnt}개')

        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'  저장: {out_path}')

    print('\n완료!')

if __name__ == '__main__':
    main()
