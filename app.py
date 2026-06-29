import streamlit as st
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# --- CSS MINIMALIS ---
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; }</style>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-6.9181&longitude=106.9266&hourly=relative_humidity_2m,uv_index&forecast_days=1"
    try:
        r = requests.get(url).json()
        return {"h": r["hourly"]["relative_humidity_2m"][:10], "uv": r["hourly"]["uv_index"][:10]}
    except:
        return {"h": [70]*10, "uv": [2]*10}

def draw_chart(draw, data, y_pos, color, is_humidity=True):
    # Disesuaikan agar jarak dan lebar lebih ramping
    start_x, jarak = 70, 95
    font = ImageFont.load_default()
    for i, val in enumerate(data):
        x = start_x + (i * jarak)
        h = (val / 100) * 200
        # Lebar balok diperkecil jadi 25 agar ramping
        draw.rounded_rectangle([x, y_pos - h, x + 25, y_pos], radius=12, fill=color)
        
        if is_humidity:
            # Lubang diperkecil agar proporsional
            draw.ellipse([x+8, y_pos - h + 8, x+17, y_pos - h + 17], fill="black")
            
        jam = (datetime.now().hour + i) % 24
        draw.text((x-5, y_pos + 20), f"{jam:02d}.00", fill="white", font=font)

# --- GENERASI GAMBAR ---
data = fetch_weather_data()
img = Image.new("RGBA", (1080, 800), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Teks di luar agar lebih tajam (menggunakan markdown di bawah)
draw.text((70, 20), "SUKABUMI REGENCY", fill="white", font=ImageFont.load_default())
draw_chart(draw, data["h"], 300, "white", is_humidity=True)
draw_chart(draw, data["uv"], 650, "yellow", is_humidity=False)

st.image(img, use_container_width=True)
