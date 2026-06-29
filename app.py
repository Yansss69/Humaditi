import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import io

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Weather Graph App", page_icon="💧", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("💧 Minimalist Weather App")

# --- LOGIKA DATA ---
@st.cache_data(ttl=3600)
def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-6.9181&longitude=106.9266&current=temperature_2m&hourly=relative_humidity_2m&forecast_days=1"
    try:
        respons = requests.get(url).json()
        return respons["hourly"]["relative_humidity_2m"][:10]
    except:
        return [71, 69, 69, 70, 73, 77, 77, 82, 87, 90]

wib = timezone(timedelta(hours=7))
jam_sekarang = datetime.now(wib)
kelembapan_list = fetch_weather_data()
waktu_list = [jam_sekarang + timedelta(hours=i) for i in range(10)]

# --- GENERASI GAMBAR ---
def create_weather_image(humidity_data, time_data):
    lebar, tinggi = 1080, 1350
    kanvas = Image.new("RGBA", (lebar, tinggi), (0, 0, 0, 0))
    draw = ImageDraw.Draw(kanvas)
    
    # Font
    f_besar = ImageFont.load_default(size=160)
    f_sedang = ImageFont.load_default(size=45)
    f_kecil_b = ImageFont.load_default(size=28)
    f_kecil_r = ImageFont.load_default(size=26)
    
    # Header & Teks Utama
    draw.text((80, 150), "SUKABUMI REGENCY", fill=(255, 255, 255, 120), font=f_sedang)
    rata_rata = int(sum(humidity_data) / len(humidity_data))
    draw.text((80, 470), f"{rata_rata}%", fill=(255, 255, 255, 255), font=f_besar)
    draw.text((80, 400), "Today's average humidity", fill=(255, 255, 255, 150), font=f_sedang)

    # Grafik Batang
    start_x, jarak, lebar_b, y_dasar, t_max = 95, 98, 32, 930, 220
    for i, p in enumerate(humidity_data):
        x1 = start_x + (i * jarak)
        y1 = y_dasar - ((p / 100) * t_max)
        draw.rounded_rectangle([x1, y1, x1 + lebar_b, y_dasar], radius=16, fill=(240, 240, 240, 255))
        
        # Label
        pusat_x = x1 + (lebar_b / 2)
        draw.text((pusat_x, y_dasar + 30), f"{p}%", fill="white", font=f_kecil_b, anchor="ma")
        label = "Now" if i == 0 else time_data[i].strftime("%H.00")
        draw.text((pusat_x, y_dasar + 70), label, fill=(255, 255, 255, 140), font=f_kecil_r, anchor="ma")

    return kanvas

# --- TAMPILAN WEB ---
img = create_weather_image(kelembapan_list, waktu_list)
st.image(img, use_container_width=True)

if st.button("🔄 Perbarui Data"):
    st.rerun()

buf = io.BytesIO()
img.save(buf, format="PNG")
st.download_button("📥 Download PNG", buf.getvalue(), "Grafik_Cuaca.png", "image/png")
