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

MEMBER_BADGE_COLORS = {
    "유니":   ("rgba(26,10,74,0.2)",    "#1a0a4a"),
    "후야":   ("rgba(255,255,255,0.15)", "#f0e6ff"),
    "히나":   ("rgba(45,0,0,0.2)",      "#2d0000"),
    "마시로": ("rgba(255,255,255,0.15)", "#ffffff"),
    "리제":   ("rgba(255,187,187,0.15)", "#ffbbbb"),
    "타비":   ("rgba(10,32,64,0.2)",    "#0a2040"),
    "시부키": ("rgba(26,0,64,0.2)",     "#1a0040"),
    "린":     ("rgba(255,255,255,0.15)", "#ffffff"),
    "나나":   ("rgba(61,0,21,0.2)",     "#3d0015"),
    "리코":   ("rgba(0,42,26,0.2)",     "#002a1a"),
}

# [수정] 상세보기 버튼 색상 - 멤버 테마 어두운 버전
MEMBER_BTN_COLORS = {
    "유니":   ("#1a0a4a", "#d4c8ff"),
    "후야":   ("#2d1a4a", "#e8d5ff"),
    "히나":   ("#2d0000", "#ffd0c8"),
    "마시로": ("#111314", "#cccccc"),
    "리제":   ("#1a0000", "#ff9999"),
    "타비":   ("#0a2040", "#c8eaff"),
    "시부키": ("#1a0040", "#e8d0ff"),
    "린":     ("#041030", "#b0d0ff"),
    "나나":   ("#3d0015", "#ffd0dd"),
    "리코":   ("#002a1a", "#a0e8c8"),
}

def load_css(path: str):
    with open(path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.dialog("상세 정보")
def show_detail(r: dict):
    name        = r["name"]
    status      = r["status"]
    pad_grad, _ = MEMBER_GRADIENTS.get(name, ("#333", "#333"))
    text_color  = MEMBER_TEXT_COLORS.get(name, "#ffffff")
    img         = r.get("img", "")

    status_kor = "🟢 방송 예정" if status == "live" else "🔴 휴방" if status == "rest" else "⚪ 공지 없음"
    time_str   = r.get("time") or "-"
    reason_str = r.get("reason") or "-"

    img_html = (
        f'<img src="{img}" style="width:80px;height:80px;border-radius:50%;object-fit:cover;margin-bottom:12px;">'
        if img else ""
    )

    st.markdown(
        f'<div style="background:{pad_grad} padding-box,{pad_grad} border-box;'
        f'border:2px solid transparent;border-radius:16px;padding:24px;text-align:center;margin-bottom:1rem;">'
        f'{img_html}'
        f'<div style="font-size:1.4rem;font-weight:700;color:{text_color};">{name}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    col1.metric("상태", status_kor)
    col2.metric("방송 시간", time_str)
    st.divider()
    st.markdown("**📝 사유**")
    st.info(reason_str)

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
    clicked = st.button("📡 오늘 방송 조회", type="primary", use_container_width=True)

if clicked:
    results = []
    progress = st.progress(0, text="조회 시작...")

    for i, (name, info) in enumerate(MEMBERS.items()):
        progress.progress((i + 1) / len(MEMBERS), text=f"{name} 확인 중...")
        menu_id = info["menu_id"]

        if not menu_id:
            results.append({
                "name": name, "img": info.get("img", ""),
                "status": "unknown", "reason": "게시판 ID 미설정", "time": None
            })
            continue

        try:
            post = fetch_today_post(menu_id)
            if post is None:
                results.append({
                    "name": name, "img": info.get("img", ""),
                    "status": "unknown", "reason": "아직 공지사항이 없습니다", "time": None
                })
            else:
                analysis = analyze_post(name, post["subject"], post["summary"], post["write_date"])
                analysis["name"] = name
                analysis["img"]  = info.get("img", "")
                results.append(analysis)
        except Exception as e:
            results.append({
                "name": name, "img": info.get("img", ""),
                "status": "error", "reason": str(e)[:40], "time": None
            })

    progress.empty()
    st.session_state["results"] = results

if "results" in st.session_state:
    results = st.session_state["results"]

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

    cols = st.columns(5)
    for i, r in enumerate(results):
        name       = r["name"]
        status     = r["status"]
        img        = r.get("img", "")
        pad_grad, border_grad = MEMBER_GRADIENTS.get(name, ("#333", "#333"))
        text_color = MEMBER_TEXT_COLORS.get(name, "#ffffff")
        badge_bg, badge_text_color = MEMBER_BADGE_COLORS.get(name, ("rgba(255,255,255,0.15)", "#ffffff"))
        btn_bg, btn_text = MEMBER_BTN_COLORS.get(name, ("#1a1a2e", "#ffffff"))

        card_class  = "live" if status == "live" else "rest" if status == "rest" else ""
        dot_class   = "dot-live" if status == "live" else "dot-rest" if status == "rest" else "dot-unknown"
        badge_text  = "방송 예정" if status == "live" else "휴방" if status == "rest" else "공지 없음"
        badge_style = f"background:{badge_bg};color:{badge_text_color};border:1px solid {badge_text_color}33;"

        # [수정] 카드 하단 border 제거 → 버튼과 시각적으로 이어지도록
        card_style = (
            f"border:2px solid transparent;"
            f"border-bottom:none;"
            f"background:{pad_grad} padding-box,{border_grad} border-box;"
        )

        # [수정] 버튼 색상 멤버별 인라인 주입
        btn_style_inject = (
            f"<style>"
            f"div[data-testid='stButton']:has(button[kind='secondary']) + div .detail-btn > button,"
            f"button[key='detail_{name}'] {{"
            f"background: {btn_bg} !important;"
            f"color: {btn_text} !important;"
            f"border-color: transparent !important;"
            f"}}</style>"
        )

        if img:
            avatar_html = f'<img class="avatar-img" src="{img}" alt="{name}">'
        else:
            avatar_style = (
                f"background:{pad_grad} padding-box,{border_grad} border-box;"
                f"border:2px solid transparent;color:{text_color};font-weight:700;"
            )
            avatar_html = f'<div class="avatar-placeholder" style="{avatar_style}">{name[0]}</div>'

        time_html = (
            f'<div class="member-time" style="color:{text_color};opacity:0.85;">🕐 {r["time"]}</div>'
            if r.get("time") else ""
        )

        card_html = (
            f'<div class="member-card {card_class}" style="{card_style}">'
            f'<div class="avatar-wrap">{avatar_html}'
            f'<div class="status-dot {dot_class}"></div></div>'
            f'<div class="member-name" style="color:{text_color};font-size:1.05rem;">{name}</div>'
            f'<span class="member-status-badge" style="{badge_style}">{badge_text}</span>'
            f'{time_html}'
            f'<div class="member-reason" style="color:{text_color};opacity:0.75;font-size:0.78rem;">{r["reason"]}</div>'
            f'</div>'
        )

        with cols[i % 5]:
            st.markdown(card_html, unsafe_allow_html=True)
            st.markdown(btn_style_inject, unsafe_allow_html=True)
            st.markdown('<div class="detail-btn">', unsafe_allow_html=True)
            if st.button("✦ 상세보기", key=f"detail_{name}", use_container_width=True):
                show_detail(r)
            st.markdown('</div>', unsafe_allow_html=True)

    KST = pytz.timezone("Asia/Seoul")
    now_str = datetime.now(KST).strftime("%Y.%m.%d %H:%M") + " KST 기준"
    st.markdown(f'<div class="update-time">🕐 {now_str}</div>', unsafe_allow_html=True)