import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
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
    start_x, jarak = 80, 100
    font = ImageFont.load_default()
    for i, val in enumerate(data):
        x = start_x + (i * jarak)
        h = (val / 100) * 150
        # Gambar Balok (Rounded Rectangle)
        draw.rounded_rectangle([x, y_pos - h, x + 40, y_pos], radius=15, fill=color)
        
        # Gambar Lubang/Titik di tengah balok (untuk kesan bolong)
        if is_humidity:
            draw.ellipse([x+15, y_pos - h + 10, x+25, y_pos - h + 20], fill="black")
            
        # Label Jam di bawah
        jam = (datetime.now().hour + i) % 24
        draw.text((x, y_pos + 30), f"{jam:02d}.00", fill="white", font=font)

# --- GENERASI GAMBAR ---
data = fetch_weather_data()
img = Image.new("RGBA", (1080, 1000), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

draw.text((80, 50), "SUKABUMI REGENCY", fill="white", font=ImageFont.load_default())
draw.text((80, 150), "Humidity", fill="white", font=ImageFont.load_default())
draw_chart(draw, data["h"], 400, "white", is_humidity=True)

draw.text((80, 600), "UV Index", fill="white", font=ImageFont.load_default())
draw_chart(draw, data["uv"], 850, "yellow", is_humidity=False)

st.image(img, use_container_width=True)

if st.button("Perbarui Data"): st.rerun()
