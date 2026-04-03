# ============================================================
# analyzer.py - Claude AI 방송/휴방 분석기
# ============================================================

import os
import json
import re
from datetime import date
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def analyze_post(member_name: str, subject: str, summary: str, write_date: str) -> dict:
    """
    카페 공지글을 분석해서 오늘 방송 여부를 판단
    - 오늘 날짜 패턴을 코드에서 먼저 감지 (Windows 호환)
    - AI에게 날짜 컨텍스트를 명시적으로 전달해 정확도 향상
    - 반환: {"status": "live|rest|unknown", "reason": str, "time": str|None}
    """
    today     = date.today()
    today_str = today.strftime("%Y년 %m월 %d일")

    # Windows 호환 날짜 패턴 생성
    m  = str(today.month)
    d  = str(today.day)
    mm = str(today.month).zfill(2)
    dd = str(today.day).zfill(2)

    today_patterns = [
        f"{m}월{d}일",
        f"{m}월 {d}일",
        f"{mm}/{dd}",
        f"{m}/{d}",
        today.strftime("%Y.%m.%d"),
        today.strftime("%Y-%m-%d"),
    ]

    # 제목 + 요약에서 오늘 날짜 패턴 탐색
    combined       = subject + " " + summary
    has_today_date = any(p in combined for p in today_patterns)
    is_today       = (write_date == today_str)

    # 분석할 텍스트 구성
    content = f"제목: {subject}"
    if summary:
        content += f"\n내용: {summary}"

    # 날짜 컨텍스트 분기
    if is_today or has_today_date:
        date_context = f"이 글은 오늘({today_str}) 방송에 대한 내용입니다."
    else:
        date_context = (
            f"이 글은 {write_date}에 작성된 글이며 오늘({today_str}) 날짜 언급이 없습니다. "
            f"오늘 방송 여부를 알 수 없으면 unknown으로 판단하세요."
        )

    prompt = f"""오늘은 {today_str}입니다.
다음은 VTuber '{member_name}'의 최신 카페 공지글입니다.

{content}

{date_context}

아래 JSON 형식으로만 응답하세요. 다른 텍스트 없이 JSON만 출력하세요.
{{"status": "live 또는 rest 또는 unknown", "reason": "사유 20자 이내", "time": "방송 시간 또는 null"}}

status 기준:
- live: 오늘 방송 예정이거나 진행 중
- rest: 오늘 휴방
- unknown: 오늘 방송 여부를 알 수 없음
"""

    res = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = res.content[0].text
    return json.loads(re.search(r"\{.*\}", raw, re.DOTALL).group())