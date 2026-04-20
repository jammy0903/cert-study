#!/usr/bin/env python3
"""TOPCIT JSON 구조 마이그레이션 - 플랫 → 중첩 계층 구조"""

import json
from pathlib import Path
from collections import defaultdict

JSON_DIR = Path(__file__).parent / "topcit_json"
OUT_DIR  = Path(__file__).parent / "topcit_json_v2"

def migrate(filepath: Path) -> dict:
    with open(filepath, encoding="utf-8") as f:
        old = json.load(f)

    # 챕터 순서 유지를 위해 old chapters 목록 사용
    chapter_order = [ch["title"] for ch in old.get("chapters", [])]

    # sections를 챕터별로 그룹핑 (순서 유지)
    chapter_sections = defaultdict(list)
    for sec in old.get("sections", []):
        ch = sec.get("chapter", "기타")
        chapter_sections[ch].append(sec)

    # 챕터 순서대로 새 구조 생성
    seen_chapters = set()
    chapters_new = []
    for ch_title in chapter_order:
        if ch_title in seen_chapters:
            continue
        seen_chapters.add(ch_title)

        sections_new = []
        for sec in chapter_sections.get(ch_title, []):
            concepts = []
            for sub in sec.get("subsections", []):
                concept = {
                    "title":       sub.get("title", ""),
                    "keywords":    sec.get("keywords", []),  # 섹션 키워드 상속
                    "background":  sub.get("background", ""),
                    "explanation": sub.get("explanation", ""),
                    "mnemonic":    sub.get("mnemonic", ""),
                }
                concepts.append(concept)

            if concepts:
                sections_new.append({
                    "title":    sec.get("title", ""),
                    "concepts": concepts,
                })

        if sections_new:
            chapters_new.append({
                "title":    ch_title,
                "sections": sections_new,
            })

    # 챕터에 없던 섹션 처리 (orphan)
    for ch_title, secs in chapter_sections.items():
        if ch_title not in seen_chapters:
            sections_new = []
            for sec in secs:
                concepts = [
                    {
                        "title":       sub.get("title", ""),
                        "keywords":    sec.get("keywords", []),
                        "background":  sub.get("background", ""),
                        "explanation": sub.get("explanation", ""),
                        "mnemonic":    sub.get("mnemonic", ""),
                    }
                    for sub in sec.get("subsections", [])
                ]
                if concepts:
                    sections_new.append({"title": sec.get("title", ""), "concepts": concepts})
            if sections_new:
                chapters_new.append({"title": ch_title, "sections": sections_new})

    return {
        "id":       old["id"],
        "title":    old["title"],
        "chapters": chapters_new,
    }


def all_concepts(data: dict):
    for ch in data["chapters"]:
        for sec in ch["sections"]:
            yield from sec["concepts"]


if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)

    for filepath in sorted(JSON_DIR.glob("topcit_0*.json")):
        new_data = migrate(filepath)
        out_path = OUT_DIR / filepath.name
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)

        chapters  = len(new_data["chapters"])
        sections  = sum(len(ch["sections"]) for ch in new_data["chapters"])
        concepts  = list(all_concepts(new_data))
        enriched  = sum(1 for c in concepts if c.get("background"))
        print(f"{filepath.name} → {chapters}챕터 / {sections}섹션 / {len(concepts)}개념  (enriched: {enriched}/{len(concepts)})")
