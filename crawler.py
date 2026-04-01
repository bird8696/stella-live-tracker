import requests
import datetime
import pytz
from config import CAFE_ID, HEADERS, COOKIES

BASE_URL = "https://apis.naver.com/cafe-web/cafe-boardlist-api/v1"
KST = pytz.timezone("Asia/Seoul")

def fetch_today_post(menu_id: str) -> dict | None:
    """최신 글 1개 반환 (작성 날짜 포함)"""
    url = f"{BASE_URL}/cafes/{CAFE_ID}/menus/{menu_id}/articles"
    params = {
        "page": 1,
        "pageSize": 3,
        "sortBy": "TIME",
        "viewType": "L",
    }

    res = requests.get(url, params=params, headers=HEADERS, cookies=COOKIES)
    res.raise_for_status()
    articles = res.json().get("result", {}).get("articleList", [])

    if not articles:
        return None

    item = articles[0].get("item", {})
    ts_ms = item.get("writeDateTimestamp", 0)
    write_dt = datetime.datetime.fromtimestamp(ts_ms / 1000, tz=KST)
    write_date = write_dt.strftime("%Y년 %m월 %d일")

    return {
        "subject": item.get("subject", "").strip(),
        "summary": item.get("summary", "").strip(),
        "write_date": write_date,
    }