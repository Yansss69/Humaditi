import streamlit as st
import requests
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import io
import math

# ==========================================
# STREAMLIT CONFIG
# ==========================================
st.set_page_config(page_title="Weather iOS", page_icon="🌤️", layout="centered")
st.markdown("""<style>.stApp{background:#000;} header,footer{visibility:hidden;}.block-container{padding-top:1rem;}</style>""", unsafe_allow_html=True)

st.title(" Weather iOS")
if st.button("🔄 Refresh"): st.rerun()

# ==========================================
# KONFIGURASI
# ==========================================
LAT, LON = -6.9181, 106.9266 # Sukabumi
CITY = "SUKABUMI REGENCY"
W, H = 1080, 1920 # Canvas size HP

# Warna
WHITE, WHITE80, WHITE60, WHITE40 = (255,255,255,255), (255,255,255,200), (255,255,255,150), (255,255,255,100)
CARD, CARD_BORDER = (255,255,255,18), (255,255,255,35)
GREEN, YELLOW, ORANGE, RED = (119,255,170,255), (255,214,10,255), (255,150,0,255), (255,60,60,255)

# ==========================================
# FONT - AUTO DOWNLOAD DARI GOOGLE FONTS
# ==========================================
@st.cache_resource
def load_font(size, bold=False):
    """Download Inter font kalau belum ada di server"""
    url = "https://github.com/rsms/inter/releases/download/v4.0/Inter-VariableFont_slnt,wght.ttf"
    try:
        font_data = requests.get(url, timeout=10).content
        weight = 700 if bold else 400
        # Inter variable font, kita pilih weight manual
        return ImageFont.truetype(io.BytesIO(font_data), size=size)
    except:
        return ImageFont.load_default() # Fallback paling aman

FONT_BIG = load_font(200, bold=True) # Suhu
FONT_BIG2 = load_font(140, bold=True) # Humidity/UV
FONT_TITLE = load_font(68, bold=True) # Status
FONT_SUB = load_font(42, bold=True) # Judul Card
FONT_SMALL = load_font(32) # Detail
FONT_MED = load_font(28) # Temp Forecast
FONT_TINY = load_font(24) # Label

# ==========================================
# AMBIL DATA CUACA
# ==========================================
@st.cache_data(ttl=600)
def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,weather_code&hourly=temperature_2m,uv_index,weather_code&daily=sunrise,sunset&forecast_days=1&timezone=Asia/Jakarta"
    try:
        d = requests.get(url, timeout=10).json()
        return {
            "temp": round(d["current"]["temperature_2m"]), "hum": round(d["current"]["relative_humidity_2m"]),
            "hum_h": d["hourly"]["relative_humidity_2m"][:10], "temp_h": d["hourly"]["temperature_2m"][:10],
            "uv_h": d["hourly"]["uv_index"][:10], "code_h": d["hourly"]["weather_code"][:10],
            "sr": d["daily"]["sunrise"][0][-5:], "ss": d["daily"]["sunset"][0][-5:],
        }
    except Exception: # Fallback kalau API error
        return {"temp": 28, "hum": 73, "hum_h": [73,72,71,70,68,65,61,58,56,54], "temp_h": [28,28,29,29,30,30,29,28,27,26], "uv_h": [5,5,5,4,3,2,1,0,0,0], "code_h": [1]*10, "sr": "05:43", "ss": "17:56"}

data = get_weather()
hours = [datetime.now() + timedelta(hours=i) for i in range(10)]

# ==========================================
# HELPER
# ==========================================
def weather_text(c):
    return {0:"Clear",1:"Partly Cloudy",2:"Partly Cloudy",3:"Cloudy"}.get(c, "Cloudy")

def uv_status(v):
    if v<=2: return "Low", GREEN
    if v<=5: return "Moderate", YELLOW
    if v<=7: return "High", ORANGE
    if v<=10: return "Very High", RED
    return "Extreme", (128,0,128,255)

def draw_icon(draw, x, y, c, s=20):
    if c==0: # Sun
        draw.ellipse((x-s,y-s,x+s,y+s),fill=YELLOW)
        for a in range(0,360,45):
            draw.line((x+math.cos(math.radians(a))*(s+4),y+math.sin(math.radians(a))*(s+4),x+math.cos(math.radians(a))*(s+12),y+math.sin(math.radians(a))*(s+12)),fill=YELLOW,width=3)
    else: # Cloud
        draw.ellipse((x-s,y-s//2,x+s//4,y+s//2),fill=WHITE)
        draw.ellipse((x-s//4,y-s,x+s,y+s//2),fill=WHITE)
        draw.rectangle((x-s,y,x+s,y+s//2),fill=WHITE)

# ==========================================
# GAMBAR CANVAS
# ==========================================
img = Image.new("RGB",(W,H),(0,0,0)); d = ImageDraw.Draw(img)

# HEADER
d.text((70,80),CITY,fill=WHITE60,font=FONT_SUB)
d.text((70,120),f"{data['temp']}°",fill=WHITE,font=FONT_BIG)
d.text((70,330),weather_text(data['code_h'][0]),fill=WHITE80,font=FONT_TITLE)
d.text((70,400),f"Humidity {data['hum']
