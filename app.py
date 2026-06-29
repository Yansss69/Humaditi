import streamlit as st
import requests
import math
import io
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(page_title="Weather iOS", page_icon="🌤️", layout="centered")
st.markdown("<style>.stApp{background:#000000;} header, footer {visibility:hidden;}</style>", unsafe_allow_html=True)

st.title(" Weather iOS")
if st.button("🔄 Refresh"): st.rerun()

# ==========================================
# CONSTANTS & CONFIG
# ==========================================
WIDTH, HEIGHT = 1080, 1920
LATITUDE, LONGITUDE = -6.9181, 106.9266
CITY = "SUKABUMI REGENCY"

# Colors
COLORS = {
    "WHITE": (255, 255, 255, 255),
    "W80": (255, 255, 255, 200),
    "W60": (255, 255, 255, 150),
    "W40": (255, 255, 255, 100),
    "W20": (255, 255, 255, 40),
    "CARD": (255, 255, 255, 18),
    "BORDER": (255, 255, 255, 35),
    "YELLOW": (255, 214, 10, 255),
    "GREEN": (119, 255, 170, 255),
    "ORANGE": (255, 150, 0, 255),
    "RED": (255, 60, 60, 255)
}

# ==========================================
# UTILITIES
# ==========================================
def get_font(size):
    try: return ImageFont.truetype("arial.ttf", size)
    except: return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

# ==========================================
# DATA FETCHING
# ==========================================
def get_weather_data():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=temperature_2m,relative_humidity_2m,weather_code&hourly=temperature_2m,relative_humidity_2m,uv_index,weather_code&daily=sunrise,sunset&forecast_days=1&timezone=Asia/Jakarta"
    try:
        res = requests.get(url, timeout=10).json()
        return {
            "temp": round(res["current"]["temperature_2m"]),
            "hum": round(res["current"]["relative_humidity_2m"]),
            "hums": res["hourly"]["relative_humidity_2m"][:10],
            "temps": res["hourly"]["temperature_2m"][:10],
            "uvs": res["hourly"]["uv_index"][:10],
            "codes": res["hourly"]["weather_code"][:10],
            "sunrise": res["daily"]["sunrise"][0][-5:],
            "sunset": res["daily"]["sunset"][0][-5:]
        }
    except:
        return {"temp": 28, "hum": 73, "hums": [70]*10, "temps": [28]*10, "uvs": [2]*10, "codes": [1]*10, "sunrise": "05:43", "sunset": "17:56"}

data = get_weather_data()

# ==========================================
# DRAWING
# ==========================================
canvas = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
d = ImageDraw.Draw(canvas)

# Header
d.text((70, 80), CITY, fill=COLORS["W60"], font=get_font(34))
d.text((70, 120), f"{data['temp']}°", fill=COLORS["WHITE"], font=get_font(170))
d.text((70, 305), "Partly Cloudy", fill=COLORS["W80"], font=get_font(56))
d.text((70, 365), f"Humidity {data['hum']}%    Sunrise {data['sunrise']}    Sunset {data['sunset']}", fill=COLORS["W60"], font=get_font(26))

# Humidity Card
draw_rounded_rect(d, (50, 450, 1030, 1050), 40, COLORS["CARD"], COLORS["BORDER"])
d.text((120, 490), "Humidity", fill=COLORS["WHITE"], font=get_font(34))
d.text((80, 610), f"{round(sum(data['hums'])/10)}%", fill=COLORS["WHITE"], font=get_font(120))

# Hourly Forecast (Visual)
for i, val in enumerate(data['hums']):
    x = 90 + i * 88
    d.rounded_rectangle((x, 940-(val*1.4), x+34, 940), radius=18, fill=(245,245,245,255))
    d.text((x+17, 970), f"{val}%", fill=COLORS["WHITE"], font=get_font(20), anchor="ma")

# Footer
d.text((WIDTH/2, HEIGHT-25), "archive by Andrian", fill=COLORS["W40"], font=get_font(26), anchor="ms")

# ==========================================
# OUTPUT
# ==========================================
st.image(canvas, use_container_width=True)
buf = io.BytesIO()
canvas.save(buf, format="PNG")
st.download_button("📥 Download PNG", buf.getvalue(), "weather.png", "image/png")
