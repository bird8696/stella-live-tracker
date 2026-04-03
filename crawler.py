# ============================================================
# crawler.py - 네이버 카페 게시글 크롤러
# ============================================================

import requests
import datetime
import re
import pytz
from config import CAFE_ID, HEADERS, COOKIES

BASE_URL = "https://apis.naver.com/cafe-web/cafe-boardlist-api/v1"
KST      = pytz.timezone("Asia/Seoul")


def fetch_today_post(menu_id: str) -> dict | None:
    """
    해당 게시판의 최신 글 1개를 가져옴
    - 날짜 필터 없이 최신 글 반환 (날짜 판단은 AI가 수행)
    - 글이 없으면 None 반환
    """
    url    = f"{BASE_URL}/cafes/{CAFE_ID}/menus/{menu_id}/articles"
    params = {
        "page":     1,
        "pageSize": 3,
        "sortBy":   "TIME",
        "viewType": "L",
    }

    res = requests.get(url, params=params, headers=HEADERS, cookies=COOKIES)
    res.raise_for_status()
    articles = res.json().get("result", {}).get("articleList", [])

    if not articles:
        return None

    item       = articles[0].get("item", {})
    ts_ms      = item.get("writeDateTimestamp", 0)
    write_date = datetime.datetime.fromtimestamp(
        ts_ms / 1000, tz=KST
    ).strftime("%Y년 %m월 %d일")

    return {
        "subject":    item.get("subject", "").strip(),
        "summary":    item.get("summary", "").strip(),
        "write_date": write_date,
        "article_id": item.get("articleId"),
    }


def fetch_article_body(article_id: int) -> str:
    """
    게시글 ID로 본문 전체 텍스트를 가져옴
    - 여러 API 엔드포인트를 순서대로 시도
    - HTML 태그 제거 후 순수 텍스트만 반환
    - 실패 시 빈 문자열 반환
    """
    if not article_id:
        return ""

    # 시도할 API 엔드포인트 목록 (순서대로 시도)
    endpoints = [
        f"https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{CAFE_ID}/articles/{article_id}",
        f"https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/{CAFE_ID}/articles/{article_id}",
        f"https://cafe.naver.com/ArticleRead.nhn?clubid={CAFE_ID}&articleid={article_id}",
    ]

    for url in endpoints:
        try:
            res = requests.get(url, headers=HEADERS, cookies=COOKIES, timeout=5)
            if res.status_code != 200:
                continue

            # JSON 응답 처리 시도
            try:
                data    = res.json()
                article = (
                    data.get("result", {}).get("article", {})
                    or data.get("article", {})
                )
                content_html = (
                    article.get("contentHtml", "")
                    or article.get("content", "")
                )
                if content_html:
                    text = re.sub(r"<[^>]+>", " ", content_html)
                    text = re.sub(r"\s+", " ", text).strip()
                    if text:
                        return text

            except Exception:
                # JSON 아니면 HTML 페이지로 파싱 시도
                from bs4 import BeautifulSoup
                soup    = BeautifulSoup(res.text, "html.parser")
                content = (
                    soup.select_one(".se-main-container")
                    or soup.select_one(".article_body")
                    or soup.select_one(".tbody")
                )
                if content:
                    text = content.get_text(separator=" ").strip()
                    text = re.sub(r"\s+", " ", text).strip()
                    if text:
                        return text

        except Exception:
            continue

    return ""