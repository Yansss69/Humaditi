import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import io

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Weather App", layout="centered")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; }</style>", unsafe_allow_html=True)

# --- FUNGSI PENGAMBILAN DATA ---
@st.cache_data(ttl=3600)
def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-6.9181&longitude=106.9266&hourly=relative_humidity_2m,uv_index&forecast_days=1"
    try:
        r = requests.get(url).json()
        return {"humidity": r["hourly"]["relative_humidity_2m"][:10], "uv": r["hourly"]["uv_index"][:10]}
    except:
        return {"humidity": [70]*10, "uv": [2]*10}

# --- FUNGSI GENERASI GAMBAR ---
def create_weather_image(data):
    lebar, tinggi = 1080, 1600
    kanvas = Image.new("RGBA", (lebar, tinggi), (0, 0, 0, 0))
    draw = ImageDraw.Draw(kanvas)
    
    # Menggunakan font bawaan agar aplikasi tidak blank
    font = ImageFont.load_default()
    
    # Header
    draw.text((80, 100), "SUKABUMI REGENCY", fill="white", font=font)
    
    # Menggambar Grafik Humidity
    start_x, jarak = 95, 98
    for i, h in enumerate(data["humidity"]):
        x = start_x + (i * jarak)
        draw.rounded_rectangle([x, 200, x + 50, 500], radius=20, fill="white")
        draw.text((x + 25, 530), f"{h}%", fill="white", font=font)

    # Menggambar Grafik UV Index
    draw.text((80, 700), "UV Index", fill="white", font=font)
    for i, uv in enumerate(data["uv"]):
        x = start_x + (i * jarak)
        warna = (255, 200, 0) if uv > 2 else (100, 255, 150)
        draw.rounded_rectangle([x, 800, x + 50, 1100], radius=20, fill=warna)
        draw.text((x + 25, 1130), str(int(uv)), fill="white", font=font)
    
    return kanvas

# --- EKSEKUSI & TAMPILAN ---
data = fetch_weather_data()
img = create_weather_image(data)
st.image(img, use_container_width=True)

if st.button("Refresh"): 
    st.rerun()
