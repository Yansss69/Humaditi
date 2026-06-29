import streamlit as st
import requests
from PIL import Image, ImageDraw
import io

# --- TAMPILAN MODERN ---
st.set_page_config(page_title="Weather App", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #ffffff; font-size: 24px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("SUKABUMI REGENCY")

@st.cache_data(ttl=3600)
def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-6.9181&longitude=106.9266&hourly=relative_humidity_2m,uv_index&forecast_days=1"
    try:
        r = requests.get(url).json()
        return {"humidity": r["hourly"]["relative_humidity_2m"][:10], "uv": r["hourly"]["uv_index"][:10]}
    except:
        return {"humidity": [70]*10, "uv": [2]*10}

# --- GRAFIK MENGGUNAKAN PILLOW ---
def create_chart(data, color, title):
    lebar, tinggi = 1080, 400
    img = Image.new("RGBA", (lebar, tinggi), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    start_x, jarak = 80, 100
    for i, val in enumerate(data):
        x = start_x + (i * jarak)
        h = (val / 100) * 300
        draw.rounded_rectangle([x, 350 - h, x + 50, 350], radius=20, fill=color)
    return img

data = fetch_weather_data()

# --- LAYOUT UI ---
st.subheader("Humidity")
st.image(create_chart(data["humidity"], "white", "Humidity"), use_container_width=True)

st.subheader("UV Index")
st.image(create_chart(data["uv"], "#FFD700", "UV Index"), use_container_width=True)

if st.button("🔄 Perbarui Data"):
    st.rerun()
