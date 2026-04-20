#!/usr/bin/env python3
"""TOPCIT JSON 개념 enrichment 스크립트 - 배경/설명/암기법 추가"""

import json
import os
import time
import anthropic
from pathlib import Path

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=API_KEY)

SYSTEM_PROMPT = """너는 친한 친구한테 공부 가르쳐주는 사람이야. IT 전공 지식이 없는 사람도 바로 이해할 수 있게 설명해줘.

주어진 IT 개념에 대해 다음 3가지를 작성해:

1. background: "옛날에 이런 문제가 있었어~" 식으로 왜 이 개념이 생겼는지 일상 언어로 2문장
2. explanation: 중학생도 이해할 수 있는 비유나 실생활 예시로 설명 2-3문장. 어려운 용어 금지.
3. mnemonic: 5초 안에 핵심을 떠올릴 수 있는 암기법 1가지 (두문자어, 짧은 스토리, 숫자, 노래 가사 패턴 등)

반드시 JSON 형식으로만 답해:
{
  "background": "...",
  "explanation": "...",
  "mnemonic": "..."
}"""

def enrich_concept(title: str, content: str, subject: str) -> dict:
    prompt = f"""과목: {subject}
개념명: {title}
원본 설명: {content[:500] if content else '(설명 없음)'}

위 개념에 대해 background, explanation, mnemonic을 JSON으로 작성해."""

    for attempt in range(3):
        try:
            msg = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=600,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            text = msg.content[0].text.strip()
            # JSON 추출
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
        except anthropic.RateLimitError:
            time.sleep(60)
        except Exception as e:
            print(f"  오류: {e}")
            time.sleep(5)
    return {"background": "", "explanation": "", "mnemonic": ""}

def process_file(filepath: Path, subject_title: str):
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    total = sum(len(s["subsections"]) for s in data["sections"])
    done = 0

    for sec in data["sections"]:
        for sub in sec["subsections"]:
            # 이미 enriched면 스킵
            if sub.get("background"):
                done += 1
                continue

            print(f"  [{done+1}/{total}] {sub['title'][:30]}...", end=" ", flush=True)
            enriched = enrich_concept(
                title=sub["title"],
                content=sub.get("content", ""),
                subject=subject_title
            )
            sub["background"] = enriched.get("background", "")
            sub["explanation"] = enriched.get("explanation", "")
            sub["mnemonic"] = enriched.get("mnemonic", "")
            done += 1
            print("✓")

            # 매 10개마다 저장 (중간 저장)
            if done % 10 == 0:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

            time.sleep(0.5)  # rate limit 방지

    # 최종 저장
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return done

SUBJECTS = {
    "topcit_01.json": "소프트웨어 개발",
    "topcit_02.json": "데이터베이스",
    "topcit_03.json": "정보보안",
    "topcit_04.json": "네트워크",
    "topcit_05.json": "시스템 소프트웨어",
    "topcit_06.json": "IT 경영",
}

if __name__ == "__main__":
    json_dir = Path(__file__).parent / "topcit_json"

    print("=== TOPCIT JSON Enrichment 시작 ===\n")
    grand_total = 0

    for filename, subject in SUBJECTS.items():
        filepath = json_dir / filename
        if not filepath.exists():
            print(f"[스킵] {filename} 없음")
            continue

        print(f"\n[{subject}] {filename}")
        count = process_file(filepath, subject)
        grand_total += count
        print(f"  → {count}개 완료, 저장됨")

    print(f"\n=== 완료: 총 {grand_total}개 개념 enrichment ===")
