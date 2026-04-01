import streamlit as st
from datetime import datetime
import pytz
from crawler import fetch_today_post
from analyzer import analyze_post
from config import MEMBERS

st.set_page_config(
    page_title="스텔라 라이브 방송 현황",
    page_icon="⭐",
    layout="wide"
)

MEMBER_GRADIENTS = {
    "유니":   ("linear-gradient(to right in oklch, #ad99f4 0%, #afa8f6 65%, #a6b7f1 100%)",
               "linear-gradient(to right in oklch, #ad99f4 0%, #afa8f6 65%, #a6b7f1 100%)"),
    "후야":   ("linear-gradient(to right in oklch, #5c4070 0%, #775396 50%, #8c75b1 100%)",
               "linear-gradient(to right in oklch, #5c4070 0%, #775396 50%, #8c75b1 100%)"),
    "히나":   ("linear-gradient(to right in oklch, #e8686b, #ff9680)",
               "linear-gradient(to right in oklch, #e8686b, #ff9680)"),
    "마시로": ("linear-gradient(to right, #25282a, #444)",
               "linear-gradient(to right, #25282a, #444)"),
    "리제":   ("linear-gradient(to right in oklch, #000, #890000)",
               "linear-gradient(to right in oklch, #000, #890000)"),
    "타비":   ("linear-gradient(to right in oklch, #89d1ff, #96baf2)",
               "linear-gradient(to right in oklch, #89d1ff, #96baf2)"),
    "시부키": ("linear-gradient(to right in oklch, #dab9fb, #bc97e8)",
               "linear-gradient(to right in oklch, #dab9fb, #bc97e8)"),
    "린":     ("linear-gradient(to right in oklch, #7abfe5, #0a4df3)",
               "linear-gradient(to right in oklch, #7abfe5, #0a4df3)"),
    "나나":   ("linear-gradient(to right in oklch, #fbb4ca, #ff8ca1)",
               "linear-gradient(to right in oklch, #fbb4ca, #ff8ca1)"),
    "리코":   ("linear-gradient(to right in oklch, #8fe1b0, #058891)",
               "linear-gradient(to right in oklch, #8fe1b0, #058891)"),
}

# 배경 밝기에 따른 텍스트 색상
MEMBER_TEXT_COLORS = {
    "유니":   "#1a0a4a",
    "후야":   "#f0e6ff",
    "히나":   "#2d0000",
    "마시로": "#ffffff",
    "리제":   "#ffbbbb",
    "타비":   "#0a2040",
    "시부키": "#1a0040",
    "린":     "#ffffff",
    "나나":   "#3d0015",
    "리코":   "#002a1a",
}

# 배경에 어울리는 배지 색상 (텍스트, 배경)
MEMBER_BADGE_COLORS = {
    "유니":   ("rgba(26,10,74,0.2)",   "#1a0a4a"),
    "후야":   ("rgba(255,255,255,0.15)", "#f0e6ff"),
    "히나":   ("rgba(45,0,0,0.2)",     "#2d0000"),
    "마시로": ("rgba(255,255,255,0.15)", "#ffffff"),
    "리제":   ("rgba(255,187,187,0.15)", "#ffbbbb"),
    "타비":   ("rgba(10,32,64,0.2)",   "#0a2040"),
    "시부키": ("rgba(26,0,64,0.2)",    "#1a0040"),
    "린":     ("rgba(255,255,255,0.15)", "#ffffff"),
    "나나":   ("rgba(61,0,21,0.2)",    "#3d0015"),
    "리코":   ("rgba(0,42,26,0.2)",    "#002a1a"),
}

def load_css(path: str):
    with open(path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

st.markdown(
    '<div class="stella-header">'
    '<div class="stella-title">✦ 스텔라 라이브 방송 현황 ✦</div>'
    '<div class="stella-subtitle">Stella Live Stream Status</div>'
    '</div>',
    unsafe_allow_html=True
)

col_btn = st.columns([1, 2, 1])
with col_btn[1]:
    clicked = st.button("📡 오늘 방송 조회", use_container_width=True)

if clicked:
    results = []
    progress = st.progress(0, text="조회 시작...")

    for i, (name, info) in enumerate(MEMBERS.items()):
        progress.progress((i + 1) / len(MEMBERS), text=f"{name} 확인 중...")
        menu_id = info["menu_id"]

        if not menu_id:
            results.append({
                "name":   name,
                "img":    info.get("img", ""),
                "status": "unknown",
                "reason": "게시판 ID 미설정",
                "time":   None
            })
            continue

        try:
            post = fetch_today_post(menu_id)
            if post is None:
                results.append({
                    "name":   name,
                    "img":    info.get("img", ""),
                    "status": "unknown",
                    "reason": "아직 공지사항이 없습니다",
                    "time":   None
                })
            else:
                analysis = analyze_post(
                    name,
                    post["subject"],
                    post["summary"],
                    post["write_date"]
                )
                analysis["name"] = name
                analysis["img"]  = info.get("img", "")
                results.append(analysis)
        except Exception as e:
            results.append({
                "name":   name,
                "img":    info.get("img", ""),
                "status": "error",
                "reason": str(e)[:40],
                "time":   None
            })

    progress.empty()

    live_n    = sum(1 for r in results if r["status"] == "live")
    rest_n    = sum(1 for r in results if r["status"] == "rest")
    unknown_n = sum(1 for r in results if r["status"] in ("unknown", "error"))

    st.markdown(
        f'<div class="metric-row">'
        f'<div class="metric-box"><div class="num num-live">{live_n}</div><div class="label">🟢 방송 예정</div></div>'
        f'<div class="metric-box"><div class="num num-rest">{rest_n}</div><div class="label">🔴 휴방</div></div>'
        f'<div class="metric-box"><div class="num num-unknown">{unknown_n}</div><div class="label">⚪ 공지 없음</div></div>'
        f'</div>',
        unsafe_allow_html=True
    )

    cards_html = '<div class="member-grid">'

    for r in results:
        name        = r["name"]
        status      = r["status"]
        img         = r.get("img", "")
        pad_grad, border_grad = MEMBER_GRADIENTS.get(name, ("#333", "#333"))
        text_color  = MEMBER_TEXT_COLORS.get(name, "#ffffff")
        badge_bg, badge_text_color = MEMBER_BADGE_COLORS.get(name, ("rgba(255,255,255,0.15)", "#ffffff"))

        card_class  = "live" if status == "live" else "rest" if status == "rest" else ""
        dot_class   = "dot-live" if status == "live" else "dot-rest" if status == "rest" else "dot-unknown"
        badge_text  = "방송 예정" if status == "live" else "휴방" if status == "rest" else "공지 없음"

        card_style = (
            f"border: 2px solid transparent;"
            f"background: {pad_grad} padding-box, {border_grad} border-box;"
        )

        if img:
            avatar_html = f'<img class="avatar-img" src="{img}" alt="{name}">'
        else:
            avatar_style = (
                f"background: {pad_grad} padding-box, {border_grad} border-box;"
                f"border: 2px solid transparent;"
                f"color: {text_color};"
                f"font-weight: 700;"
            )
            avatar_html = f'<div class="avatar-placeholder" style="{avatar_style}">{name[0]}</div>'

        time_html = (
            f'<div class="member-time" style="color:{text_color};opacity:0.85;">🕐 {r["time"]}</div>'
            if r.get("time") else ""
        )

        badge_style = (
            f"background:{badge_bg};"
            f"color:{badge_text_color};"
            f"border: 1px solid {badge_text_color}33;"
        )

        card = (
            f'<div class="member-card {card_class}" style="{card_style}">'
            f'<div class="avatar-wrap">{avatar_html}'
            f'<div class="status-dot {dot_class}"></div></div>'
            f'<div class="member-name" style="color:{text_color};font-size:1.05rem;">{name}</div>'
            f'<span class="member-status-badge" style="{badge_style}">{badge_text}</span>'
            f'{time_html}'
            f'<div class="member-reason" style="color:{text_color};opacity:0.75;font-size:0.78rem;">{r["reason"]}</div>'
            f'</div>'
        )
        cards_html += card

    cards_html += '</div>'

    KST = pytz.timezone("Asia/Seoul")
    now_str = datetime.now(KST).strftime("%Y.%m.%d %H:%M") + " KST 기준"

    st.markdown(cards_html, unsafe_allow_html=True)
    st.markdown(
        f'<div class="update-time">🕐 {now_str}</div>',
        unsafe_allow_html=True
    )