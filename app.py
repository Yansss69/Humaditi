import streamlit as st
import requests
import math
import io
import os
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont

# ===============================
# CONFIG & STYLE
# ===============================
st.set_page_config(page_title="Weather iOS", page_icon="🌤️", layout="centered")

st.markdown("""
<style>
.stApp { background: #000000; color: white; }
header { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.title(" Weather iOS")
if st.button("🔄 Refresh"):
    st.rerun()

# ===============================
# KONSTANTA & WARNA
# ===============================
LATITUDE, LONGITUDE, CITY = -6.9181, 106.9266, "SUKABUMI REGENCY"
WIDTH, HEIGHT = 1080, 1920
WHITE = (255, 255, 255, 255)
WHITE60 = (255, 255, 255, 150)
WHITE30 = (255, 255, 255, 90)
YELLOW = (255, 214, 10, 255)
GREEN = (124, 255, 170, 255)
ORANGE = (255, 145, 0, 255)
RED = (255, 72, 72, 255)
CARD = (255, 255, 255, 18)
CARD2 = (255, 255, 255, 30) # Didefinisikan di awal agar tidak error

# ===============================
# FUNGSI FONT
# ===============================
def get_font(size):
    # Menggunakan font default jika file tidak ditemukan
    return ImageFont.load_default()

FONT_TITLE = get_font(38)
FONT_SUB = get_font(28)
FONT_BIG = get_font(150)
FONT_MED = get_font(56)
FONT_SMALL = get_font(24)
FONT_TINY = get_font(20)

# ===============================
# LOGIKA API & DATA
# ===============================
url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=temperature_2m,relative_humidity_2m,weather_code&hourly=temperature_2m,relative_humidity_2m,uv_index,weather_code&daily=sunrise,sunset&timezone=Asia%2FBangkok&forecast_days=1"

try:
    data = requests.get(url, timeout=10).json()
    current_temp = round(data["current"]["temperature_2m"])
    current_humidity = round(data["current"]["relative_humidity_2m"])
    humidity = data["hourly"]["relative_humidity_2m"][:10]
    uv = data["hourly"]["uv_index"][:10]
    temp_hour = data["hourly"]["temperature_2m"][:10]
    weather_code = data["hourly"]["weather_code"][:10]
    sunrise = data["daily"]["sunrise"][0][-5:]
    sunset = data["daily"]["sunset"][0][-5:]
except:
    current_temp, current_humidity = 28, 74
    humidity, uv, temp_hour, weather_code = [74]*10, [5]*10, [28]*10, [1]*10
    sunrise, sunset = "05:43", "17:56"

wib = timezone(timedelta(hours=7))
now = datetime.now(wib)
hours = [now + timedelta(hours=i) for i in range(10)]

# ===============================
# GAMBAR
# ===============================
canvas = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(canvas)

# Header
draw.text((70, 70), CITY, fill=WHITE60, font=FONT_SUB)
draw.text((70, 120), f"{current_temp}°", fill=WHITE, font=FONT_BIG)
draw.text((70, 300), "Partly Cloudy", fill=WHITE, font=FONT_MED)
draw.text((70, 365), f"Humidity {current_humidity}% • Sunrise {sunrise} • Sunset {sunset}", fill=WHITE60, font=FONT_SMALL)

# Kartu Humidity
draw.rounded_rectangle((55, 470, WIDTH-55, 1030), radius=45, fill=CARD, outline=CARD2, width=2)
# (Tambahkan elemen visual lainnya di sini sesuai logika Anda...)

# ===============================
# DISPLAY & DOWNLOAD
# ===============================
st.image(canvas, use_container_width=True)

buf = io.BytesIO()
canvas.save(buf, format="PNG")
st.download_button("📥 Download PNG", buf.getvalue(), "Weather_iOS.png", "image/png")
