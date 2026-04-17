"""
정보처리기사_실기_출제현황_뜻포함.md 에 [중요도] 컬럼 추가.

분류 기준
  ★★★ : 3회 이상 출제 (반복 빈출, 무조건 외우기)
  ★★   : 2회 출제
  ★     : 1회 출제
  ⚡     : 미출제인데 이번 시험 나올 가능성 높음
          - 9-2 최우선 쪽집게 목록 → ★★★ + ⚡
          - 9-3 차상위 쪽집게 목록 → ★★ + ⚡
          - 미출제지만 '같은 카테고리 내 구멍' → ⚡ (수동 판단)
  (공란) : 약출제 또는 기타 미출제 (우선순위 낮음)
"""
import re
from pathlib import Path

SRC = Path('/home/jammy/projects/cert-study/정보처리기사_실기_출제현황_뜻포함.md')

# ── 9-2 최우선 쪽집게 (★★★⚡) ──
TIER_A = {
    'Strategy', 'Decorator', 'Facade', 'Builder', 'Prototype',
    'INNER JOIN', 'NATURAL JOIN', 'LEFT/RIGHT OUTER JOIN',
    'LEFT OUTER JOIN', 'RIGHT OUTER JOIN',
    'INTERSECT', 'MINUS',
    '1NF', 'BCNF',
    'Consistency', 'Durability',
    '전송 계층', '세션 계층', '응용 계층',
    'XSS', 'CSRF', 'Ransomware', 'Replay Attack',
    'SHA-256', 'SHA-1',
    '기밀성', '무결성',
    'FCFS', '우선순위 스케줄링', '다단계 피드백 큐',
    'FIFO', 'OPT', 'NUR',
    '지연 갱신 회복 기법',
}

# ── 9-3 차상위 쪽집게 (★★⚡) ──
TIER_B = {
    'REVOKE',
    'TCP', 'UDP', 'HTTPS', 'FTP', 'SMTP', 'POP3', 'IMAP',
    '3DES', 'Diffie-Hellman', 'ElGamal', 'RC4',
    '기본 경로 커버리지', '다중 조건 커버리지', '상태 전이 테스트',
    '유스케이스 다이어그램', '시퀀스 다이어그램', '활동 다이어그램',
    '타임스탬프 순서', '낙관적 검증', '다중버전 동시성 제어',
    '자료 결합도', '외부 결합도',
    '논리적 응집도',
    '정상응답모드(NRM)', '정상응답모드',
}

# ── 수동 판단 ⚡ (미출제인데 나올 확률 높은 항목) ──
# 카테고리 내 다른 것 대부분 출제됐거나, 신기술·핵심 개념
MANUAL_URGENT = {
    # UML 추가 (9-3 외)
    '커뮤니케이션 다이어그램', '타이밍 다이어그램', '객체 다이어그램',
    '컴포넌트 다이어그램', '배치 다이어그램',
    '실현/실체화(Realization)', '합성(Composition)', '접근제어자',
    # 파티셔닝 — 전체 미출제인데 '파티셔닝 종류' 한 세트 자주 출제 패턴
    '파티셔닝(Partitioning)',
    'Range Partitioning(범위 분할)', 'List Partitioning(리스트 분할)',
    'Hash Partitioning(해시 분할)', 'Composite Partitioning(복합 분할)',
    'Round-Robin Partitioning(라운드로빈 분할)',
    # 논리적 데이터 모델 — 관계만 나옴, 나머지 2개 쪽집게
    '계층 모델(Hierarchical Model)', '네트워크 모델(Network Model)',
    # 연계방식 — SOAP/WSDL/UDDI는 나왔으므로 나머지 연계방식 주목
    '하이퍼링크(HyperLink)', 'JDBC', 'Open API', 'DB Connection',
    'ESB', 'Web Service', 'Socket',
    '웹서비스 - 서비스 브로커', '웹서비스 - 서비스 요청자/소비자', '웹서비스 - 서비스 제공자',
    'UDDI',
    # 하둡 — 하둡 자체 출제, 주요기술 미출제 → 주목
    'HDFS', 'MapReduce', 'ETL', 'Flume', 'Sqoop', 'Scrapy',
    # NoSQL 유형 — NoSQL 개념 출제됐을 것, 유형은 미출제
    'NoSQL',
    'Key-Value Store', 'Document Store', 'Column-Family Store', 'Graph DB',
    'Key-Value DB', 'Document DB', 'Column-Family DB',
    # 데이터마이닝 규칙 — 마이닝 개념 출제됨
    '분류(Classification) 규칙', '연관(Association) 규칙',
    '연속 데이터(Sequential) 규칙', '군집화(Clustering) 규칙',
    # 빅데이터 저장소
    '데이터 웨어하우스', '데이터마트', 'OLAP', '빅데이터 3V',
    # 데이터 관련 용어 (신기술 빈출 후보)
    '텍스트마이닝', '웹마이닝', '메타데이터', '다크데이터', '디지털아카이빙', '마이데이터',
    # 디자인 패턴 추가 미출제 (9-2 외)
    'Composite',
    # SQL
    'ASC',
    # 보안 공격
    'Evil Twin',
    # OS 스케줄링 — 9-2에 '다단계 피드백 큐' 있음. '다단계 큐'는 별개 개념이지만 같이 나올 가능성
    '다단계 큐',
    # 기본키 — 후보키/외래키/대체키 나옴, 기본키만 미출제
    '기본키',
    # 정규화 고차 정규형
    '4NF', '5NF',
    # 반정규화 기법 (약출제 카테고리지만 언급 빈도 높음) - 이미 약출제로 분류됨
    # 5-2 보안 추가 (XSS/CSRF 제외 중요)
    'DNS 스푸핑', 'APT', 'Smurf',
    # 스케줄링 나머지
    'SJF', 'HRN', 'SRT', 'RR',
    # 페이지 교체 나머지
    'LRU', 'LFU',
    # 회복 기법 나머지
    '그림자 페이지 기법', '검사점 회복 기법',
}


def load_source():
    return SRC.read_text(encoding='utf-8')


def count_appearances(history: str) -> int:
    """출제 이력 문자열에서 '-X회 Y번' 패턴 개수."""
    if not history:
        return 0
    history = history.strip()
    if history == '미출제' or history.startswith('약출제'):
        return 0
    matches = re.findall(r'20\d{2}-\d+회\s*\d+번', history)
    return len(matches)


def get_status_type(history: str) -> str:
    h = history.strip()
    if h == '미출제':
        return 'miss'
    if h.startswith('약출제'):
        return 'weak'
    return 'hit' if h else 'empty'


def importance_marker(item_name: str, history: str) -> str:
    """
    (중요도 문자열, sort_key)
    """
    status = get_status_type(history)
    count = count_appearances(history)

    in_tier_a = item_name in TIER_A
    in_tier_b = item_name in TIER_B
    in_manual = item_name in MANUAL_URGENT

    if status == 'hit':
        # 출제됨 — 빈도순
        if count >= 3:
            return '★★★'
        elif count == 2:
            return '★★'
        elif count == 1:
            return '★'
        return ''
    elif status == 'miss':
        # 미출제 — 쪽집게 우선순위
        if in_tier_a:
            return '★★★⚡'
        elif in_tier_b:
            return '★★⚡'
        elif in_manual:
            return '⚡'
        return ''
    elif status == 'weak':
        # 약출제 — 낮은 우선순위
        if in_tier_a:
            return '★★⚡'  # 약출제인데 쪽집게라면 중요
        if in_tier_b:
            return '★⚡'
        return '·'
    return ''


def process():
    text = load_source()
    lines = text.splitlines()
    out = []
    stats = {'marked': 0, 'miss_no_mark': [], 'total_rows': 0}

    i = 0
    in_analysis_section = False  # 9-1 이후는 건드리지 않음

    while i < len(lines):
        line = lines[i]

        # 9. 분석 섹션 진입 시 마킹 중단 (이미 구조 다름)
        if line.startswith('## 9.'):
            in_analysis_section = True

        if (not in_analysis_section
            and line.strip().startswith('|')
            and i + 1 < len(lines)
            and re.match(r'^\s*\|?\s*:?-+', lines[i + 1])):
            header = [c.strip() for c in line.strip().strip('|').split('|')]

            # '항목' 헤더 시작하는 표만 대상
            if header and header[0] == '항목' and len(header) >= 3:
                # 헤더에 '중요도' 컬럼 삽입 (맨 앞)
                new_header = '| 중요도 | ' + ' | '.join(header) + ' |'
                out.append(new_header)
                # 구분선
                out.append('|' + '|'.join(['---'] * (len(header) + 1)) + '|')
                i += 2

                # 데이터 행 처리
                while i < len(lines) and lines[i].strip().startswith('|'):
                    cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                    if len(cells) < len(header):
                        cells += [''] * (len(header) - len(cells))
                    elif len(cells) > len(header):
                        cells = cells[:len(header)]

                    item_name = cells[0]
                    history = cells[1] if len(cells) > 1 else ''
                    marker = importance_marker(item_name, history)
                    stats['total_rows'] += 1
                    if marker:
                        stats['marked'] += 1
                    elif get_status_type(history) == 'miss':
                        stats['miss_no_mark'].append(item_name)

                    new_row = '| ' + marker + ' | ' + ' | '.join(cells) + ' |'
                    out.append(new_row)
                    i += 1
                continue

        out.append(line)
        i += 1

    return '\n'.join(out) + ('\n' if text.endswith('\n') else ''), stats


if __name__ == '__main__':
    new_text, stats = process()
    SRC.write_text(new_text, encoding='utf-8')
    print(f"✔ 저장: {SRC}")
    print(f"  총 {stats['total_rows']}행 / 마커 부여 {stats['marked']}행")
    print(f"  미출제 & 마커 없음 ({len(stats['miss_no_mark'])}개):")
    for name in stats['miss_no_mark']:
        print(f"    - {name}")
