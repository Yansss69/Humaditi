import streamlit as st
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Weather App", layout="centered")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; }</style>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-6.9181&longitude=106.9266&current=temperature_2m&hourly=relative_humidity_2m,uv_index,weather_code&forecast_days=1"
    try:
        r = requests.get(url).json()
        return {
            "h": r["hourly"]["relative_humidity_2m"][:10],
            "uv": r["hourly"]["uv_index"][:10],
            "temp": r["current"]["temperature_2m"]
        }
    except:
        return {"h": [70]*10, "uv": [2]*10, "temp": 28}

# --- FUNGSI GRAFIS ---
def draw_chart(data, color, is_humidity=True):
    img = Image.new("RGBA", (1080, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    start_x, jarak = 60, 100
    for i, val in enumerate(data):
        x = start_x + (i * jarak)
        h = (val / 100) * 150
        # Balok
        draw.rounded_rectangle([x, 200 - h, x + 30, 200], radius=15, fill=color)
        # Detail Tetesan Air
        if is_humidity:
            # Lingkaran kecil di atas balok untuk kesan tetesan air
            draw.ellipse([x+8, 200 - h - 10, x+22, 200 - h + 4], fill="white")
    return img

# --- TAMPILAN WEB ---
data = fetch_weather_data()
st.title("SUKABUMI REGENCY")
st.metric("Temperature Sekarang", f"{data['temp']}°C")

st.subheader("Humidity (%)")
st.image(draw_chart(data["h"], "white", True), use_container_width=True)

st.subheader("UV Index")
st.image(draw_chart(data["uv"], "#FFD700", False), use_container_width=True)

# Footer Detail
st.write("---")
st.caption("Data diperbarui setiap jam dari Open-Meteo API.")
if st.button("🔄 Perbarui"): st.rerun()
