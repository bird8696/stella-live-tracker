import os
from dotenv import load_dotenv

load_dotenv()

CAFE_ID = "29424353"

MEMBERS = {
    "유니":   {"menu_id": "134", "img": "https://i.namu.wiki/i/fTVKorkopUL8Tn6Q4VfejJ7o9_pokc3iUWIEduy9EEBoUGO0AIOyw6VJFb3RoNCDYg1Ve7ydefkRRWwf7kvGEc5Ihmy7CyTABkqkTLk_MbrZ8lQ9uUIs6GtS9H4mL4U_Z6jdQCGYTPyzo0m4GKKKvg.webp"},
    "후야":   {"menu_id": "382", "img": "https://i.namu.wiki/i/0KOE7yT99AEJ2gKOgqVM7NupK2ny1QcXDswg1W5rBJxgTIQFXUcYdIuM3rvWj-Chp8vQFrUskHSLS8CKKiMBXX8FzNR-jRY92OMXmX6RwbW86pV4b6hf3UTNNY-MEiYwFEeXTE_B3actNiqk62vOTQ.webp"},
    "히나":   {"menu_id": "149", "img": "https://i.namu.wiki/i/rMtPEVJd0euNhAL7yrPQvUfUVmRIdpzeTGWMBLq8CDzy2XzUywgXHbGZO5cwaCHydKqZlD6o4kRfo-rnxtf57McusYXrCgLfxVOxGS5pfiRLq9EtEbDWQOy7Nz0Ba6w_qLwnwIftmbofTdFy2jqbDw.webp"},
    "마시로": {"menu_id": "150", "img": "https://i.namu.wiki/i/v2oqguzfO1ZldccsQa8S-WICMjSz6YrPig_ctnWhCCuJdv0ir0YOuByEoDOZDW7hSZ5CyVDUJxtna2h5nOTPMGT37KkH9FUtxEIvpZwABJ4UJUOdn8k0R5ObsPQtEjl6jnW5ckdxSqJt4srm-jXdBA.webp"},
    "리제":   {"menu_id": "151", "img": "https://i.namu.wiki/i/HCh33dv_wByguH0fF3myKAfaHCv3l5px1srP-3dm9dzFEYeY-xB6_EboClo1ikAovRy6j8izTLz2sWBQEGSXKrahbgxrkAErZ3J7IrtgGTse2U5vOjCkv4-KwlcfM1N8s6bGyiO4t02QY1HE1oan9g.webp"},
    "타비":   {"menu_id": "152", "img": "https://i.namu.wiki/i/RDUaSG_PHGXPiY6PuevJ-2looppMcCnmVu0VNWDwxbPxvRh_EsmMJOayzZK3oXR4oWvo4lNbkCJKZ9Q3vqL0elD6zOd5HKUhwrtNcIaLP3pJud3nbTgY4KjZ9wMAFy03gsEOtFr6cmiHndFpiQnQtQ.webp"},
    "시부키": {"menu_id": "250", "img": "https://i.namu.wiki/i/hbMSZ3YqMBVOanNmiN8DZqRO0VePco2cxjhuThEqweqTGYUYsrWYTZS8m3q_bmeN8b4xa1f5QecpvHVEy0dp5fksuQoj_iAaUweUv2Ktm8g0QW4nqBppyXeRUrIaYTt2ra0VN0-A45vTUDSXcZ0hgg.webp"},
    "린":     {"menu_id": "251", "img": "https://i.namu.wiki/i/fhQdY33fel4KbTTYViXgm-D_EqhFm-PeZeUros5TsS_fX5ryDfZuDK8yBFzMu6bwqXvqrOcmvuLEib4orjLcl4fE1Goh4YAGYYdluE6wbHUs-rP_d83BUZqL09nWXeKgNbQv0_mRvs4Muw6-KjJoCQ.webp"},
    "나나":   {"menu_id": "252", "img": "https://i.namu.wiki/i/p--lMQh6EuSipaiHctLBGJVwHwIUQq4wsWNnrMTC1muQZOj2dK19oIxY3WiiIk8erwbYvFTybIb9J14xUuZGeDNAeeoMsmnVNCdwswx3-Z8jZHt_rij0q0oyddFh11umAfqHYMVLg7RUIUC3WLEFtw.webp"},
    "리코":   {"menu_id": "253", "img": "https://i.namu.wiki/i/rTR-7akJ95ON1Aj7jsVMPFZrHT8MsRNZKPEERK8F_2DqtgvzQLH15Yrn07Kxiw5ZEqgsMsVOl6vDQDakhin6kMStDz8wstcNvWQtfF9FvuYXENSjts4xxbwx7zOcL3eI1PVPPc-vtQBGp4udBI4b5w.webp"},
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://cafe.naver.com/",
    "Accept": "application/json",
}

COOKIES = {
    "NID_AUT":    os.getenv("NAVER_NID_AUT"),
    "NID_SES":    os.getenv("NAVER_NID_SES"),
    "JSESSIONID": os.getenv("NAVER_JSESSIONID"),
}