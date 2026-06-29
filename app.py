import streamlit as st
import requests
import io
import math
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# CONFIG & STYLE
# ==========================================
st.set_page_config(page_title="Weather iOS", layout="centered")
st.markdown("""
<style>
    .stApp { background: #000000; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.title(" Weather iOS")
if st.button("🔄 Refresh"): st.rerun()

# ==========================================
# FONT HELPER (Lebih besar & Jelas)
# ==========================================
def get_font(size):
    try:
        # Prioritaskan font yang lebih tebal/jelas
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

# ==========================================
# CANVAS SETUP
# ==========================================
WIDTH, HEIGHT = 1080, 1920
canvas = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(canvas)

# Data (Menggunakan data Anda)
current_temp, current_humidity = 28, 73
status = "Partly Cloudy"
sunrise, sunset = "05:43", "17:56"

# ==========================================
# RENDERING
# ==========================================

# 1. Header (Diperbesar)
draw.text((70, 80), "SUKABUMI REGENCY", fill=(255,255,255,160), font=get_font(40))
draw.text((70, 140), f"{current_temp}°", fill=(255,255,255,255), font=get_font(200))
draw.text((70, 350), status, fill=(255,255,255,220), font=get_font(65))
draw.text((70, 420), f"Humidity {current_humidity}%  •  Sunrise {sunrise}  •  Sunset {sunset}", fill=(255,255,255,160), font=get_font(30))

# 2. Reusable Card Function
def draw_styled_card(y_top, y_bottom, title):
    draw.rounded_rectangle((50, y_top, WIDTH-50, y_bottom), radius=50, fill=(255,255,255,25), outline=(255,255,255,40), width=2)
    draw.text((100, y_top + 30), title, fill=(255,255,255,255), font=get_font(40))

# 3. Humidity Card
draw_styled_card(500, 1050, "Humidity")
draw.text((100, 600), f"{current_humidity}%", fill=(255,255,255,255), font=get_font(140))
draw.text((100, 720), "Today's average humidity level", fill=(255,255,255,150), font=get_font(30))

# 4. UV Card
draw_styled_card(1100, 1600, "UV Index")
draw.text((100, 1200), "5", fill=(255,255,255,255), font=get_font(140))
draw.text((250, 1260), "Moderate", fill=(255,255,255,255), font=get_font(60))

# 5. Footer
draw.text((WIDTH/2, HEIGHT-60), "archive by Andrian", fill=(255,255,255,100), font=get_font(30), anchor="ms")

# ==========================================
# DISPLAY
# ==========================================
st.image(canvas, use_container_width=True)

# Download
buf = io.BytesIO()
canvas.save(buf, format="PNG")
st.download_button("📥 Download PNG", buf.getvalue(), "weather_ios.png", "image/png")
