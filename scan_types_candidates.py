#!/usr/bin/env python3
"""섹션 단위로 분류형 구조를 추출.
각 section마다:
  - 형제 concept들이 어떤 제목 패턴을 공유하는지
  - "A 종류/유형/분류" 같은 개념이 있는지
  - '단일 상위 개념 + 여러 sub-type'으로 볼 만한 그룹인지
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).parent
JSON_DIR = ROOT / "topcit_json_v2"

# 강한 신호(제목)
STRONG_TITLE = re.compile(
    r"(응집도|결합도|생명주기|모델\b|기법|방식|구조|정규화|정규형|스케줄|프로토콜|계층|"
    r"접근통제|암호|공격|토폴로지|아키텍처|패턴|RAID|ACID|트랜잭션|"
    r"종류|유형|분류|단계|원칙|요소|특성|특징)"
)


def load(subj_id):
    with open(JSON_DIR / f"topcit_{subj_id}.json", encoding="utf-8") as f:
        return json.load(f)


def section_report(ch_title, sec):
    titles = [c.get("title", "") for c in sec["concepts"]]
    n = len(titles)
    if n == 0:
        return None

    # 형제 공통 접미사/접두사 탐지 (e.g. '삽입 이상', '삭제 이상', '수정 이상')
    def common_suffix(titles):
        if len(titles) < 2: return ""
        # 끝에서부터 공통
        rev = [t[::-1] for t in titles]
        common = rev[0]
        for t in rev[1:]:
            new = []
            for a, b in zip(common, t):
                if a == b: new.append(a)
                else: break
            common = "".join(new)
        return common[::-1]

    def common_prefix(titles):
        if len(titles) < 2: return ""
        common = titles[0]
        for t in titles[1:]:
            new = []
            for a, b in zip(common, t):
                if a == b: new.append(a)
                else: break
            common = "".join(new)
        return common

    suf = common_suffix(titles).strip()
    pre = common_prefix(titles).strip()
    if len(suf) < 2: suf = ""
    if len(pre) < 2: pre = ""

    # 섹션 안에 이미 enriched된 개념
    enriched = [c["title"] for c in sec["concepts"] if c.get("types")]

    # 강한 신호 제목
    strong = [t for t in titles if STRONG_TITLE.search(t)]

    return {
        "chapter": ch_title,
        "section": sec["title"],
        "n": n,
        "titles": titles,
        "common_suffix": suf,
        "common_prefix": pre,
        "strong_titles": strong,
        "enriched": enriched,
    }


def main():
    for i in range(1, 7):
        subj_id = f"0{i}"
        data = load(subj_id)
        print(f"\n{'#'*72}")
        print(f"# {subj_id} {data['title']}")
        print(f"{'#'*72}")
        for ch in data["chapters"]:
            print(f"\n## [CH] {ch['title']}")
            for sec in ch["sections"]:
                r = section_report(ch["title"], sec)
                if r is None: continue
                # 흥미로운 섹션만 출력: 강한 제목 있거나, 공통 접미사/접두사가 의미있거나
                interesting = bool(r["strong_titles"]) or bool(r["common_suffix"]) or bool(r["enriched"])
                if not interesting: continue
                mark = "✅" if r["enriched"] else "  "
                print(f"  {mark} §{r['section']}  (n={r['n']})")
                if r["common_suffix"]:
                    print(f"       공통접미사: '{r['common_suffix']}'")
                if r["common_prefix"]:
                    print(f"       공통접두사: '{r['common_prefix']}'")
                for t in r["titles"]:
                    m = "★" if t in r["strong_titles"] else ("✅" if t in r["enriched"] else "·")
                    print(f"       {m} {t}")


if __name__ == "__main__":
    main()
