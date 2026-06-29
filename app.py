import streamlit as st
import requests
from datetime import datetime
from PIL import Image, ImageDraw
import io

# --- CSS MINIMALIS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; font-family: sans-serif; }
    .metric-value { font-size: 40px; font-weight: bold; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-6.9181&longitude=106.9266&current=temperature_2m&hourly=relative_humidity_2m,uv_index&forecast_days=1"
    r = requests.get(url).json()
    return {
        "temp": r["current"]["temperature_2m"],
        "h": r["hourly"]["relative_humidity_2m"][:10],
        "uv": r["hourly"]["uv_index"][:10]
    }

def draw_bars(data, color, is_humidity=True):
    # Menggambar grafis saja
    img = Image.new("RGBA", (1000, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for i, val in enumerate(data):
        x = 50 + (i * 95)
        h = (val / 100) * 150
        # Balok ramping
        draw.rounded_rectangle([x, 200 - h, x + 30, 200], radius=15, fill=color)
        if is_humidity:
            # Titik "bolong" di atas
            draw.ellipse([x+8, 200 - h + 5, x+22, 200 - h + 19], fill="black")
    return img

data = get_data()

# --- LAYOUT UI ---
st.write(f"Temperature Sekarang")
st.markdown(f"<div class='metric-value'>{data['temp']}°C</div>", unsafe_allow_html=True)

st.write("Humidity (%)")
st.image(draw_bars(data['h'], "white", True), use_container_width=True)

st.write("UV Index")
st.image(draw_bars(data['uv'], "#FFD700", False), use_container_width=True)

# Footer
st.write("---")
st.caption("Data diperbarui tiap jam • archive by Andrian")
if st.button("🔄 Perbarui"): st.rerun()
