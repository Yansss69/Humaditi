import streamlit as st
import requests
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import io
import math

# ==========================================
# STREAMLIT CONFIG
# ==========================================
st.set_page_config(
    page_title="Weather iOS",
    page_icon="🌤️",
    layout="centered"
)

st.markdown("""
<style>
.stApp{ background:#000; }
header{ visibility:hidden; }
footer{ visibility:hidden; }
.block-container{ padding-top: 1rem; padding-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

st.title(" Weather iOS")

if st.button("🔄 Refresh"):
    st.rerun()

# ==========================================
# KONFIGURASI
# ==========================================
LATITUDE = -6.9181 # Sukabumi
LONGITUDE = 106.9266
CITY = "SUKABUMI REGENCY"
TIMEZONE = "Asia/Jakarta"

# Warna
WHITE = (255,255,255,255)
WHITE80 = (255,255,255,200)
WHITE60 = (255,255,255,150)
WHITE40 = (255,255,255,100)
WHITE20 = (255,255,255,40)
CARD = (255,255,255,18)
CARD_BORDER = (255,255,255,35)
GREEN = (119,255,170,255)
YELLOW = (255,214,10,255)
ORANGE = (255,150,0,255)
RED = (255,60,60,255)

# ==========================================
# FONT - UDAH DIGEDEIN SEMUA
# ==========================================
def load_font(size):
    """Coba load SF Pro, kalau gagal pakai DejaVu/Arial"""
    font_paths = [
        "SF-Pro-Display-Bold.otf",
        "SF-Pro-Display-Regular.otf",
        "SFProDisplay-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "arial.ttf"
    ]
    for f in font_paths:
        try:
            return ImageFont.truetype(f, size)
        except:
            continue
    return ImageFont.load_default()

FONT_BIG = load_font(200) # Suhu besar
FONT_TITLE = load_font(68) # Status cuaca
FONT_SUB = load_font(42) # Judul Card
FONT_SMALL = load_font(32) # Detail
FONT_MED = load_font(28) # Jam/Temp forecast
FONT_TINY = load_font(24) # Label kecil

# ==========================================
# API DATA
# ==========================================
@st.cache_data(ttl=600) # Cache 10 menit biar gak spam API
def get_weather_data():
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}"
        "&current=temperature_2m,relative_humidity_2m,weather_code"
        "&hourly=temperature_2m,relative_humidity_2m,uv_index,weather_code"
        "&daily=sunrise,sunset"
        "&forecast_days=1"
        f"&timezone={TIMEZONE}"
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        d = r.json()
        return {
            "current_temp": round(d["current"]["temperature_2m"]),
            "current_humidity": round(d["current"]["relative_humidity_2m"]),
            "humidity": d["hourly"]["relative_humidity_2m"][:10],
            "temperature": d["hourly"]["temperature_2m"][:10],
            "uv": d["hourly"]["uv_index"][:10],
            "weather": d["hourly"]["weather_code"][:10],
            "sunrise": d["daily"]["sunrise"][0][-5:],
            "sunset": d["daily"]["sunset"][0][-5:],
        }
    except Exception:
        # Fallback data kalau offline
        return {
            "current_temp": 28, "current_humidity": 73,
            "humidity": [73,72,71,70,68,65,61,58,56,54],
            "temperature": [28,28,29,29,30,30,29,28,27,26],
            "uv": [5,5,5,4,3,2,1,0,0,0],
            "weather": [1]*10,
            "sunrise": "05:43", "sunset": "17:56",
        }

data = get_weather_data()
now = datetime.now()
hours = [now + timedelta(hours=i) for i in range(10)]

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def weather
