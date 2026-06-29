import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import io

# ... (CSS dan Setup sama seperti sebelumnya) ...

@st.cache_data(ttl=3600)
def fetch_weather_data():
    # Menambahkan uv_index_max ke dalam parameter API
    url = "https://api.open-meteo.com/v1/forecast?latitude=-6.9181&longitude=106.9266&current=temperature_2m&hourly=relative_humidity_2m,uv_index&forecast_days=1"
    try:
        respons = requests.get(url).json()
        data = {
            "humidity": respons["hourly"]["relative_humidity_2m"][:10],
            "uv": respons["hourly"]["uv_index"][:10]
        }
        return data
    except:
        return {"humidity": [71]*10, "uv": [5, 5, 5, 3, 2, 0, 0, 0, 0, 0]}

# ... (Logika waktu tetap sama) ...

def create_weather_image(data, time_data):
    lebar, tinggi = 1080, 1600 # Tinggi ditambah untuk memuat UV
    kanvas = Image.new("RGBA", (lebar, tinggi), (0, 0, 0, 0))
    draw = ImageDraw.Draw(kanvas)
    f_sedang = ImageFont.load_default(size=45)
    f_kecil_b = ImageFont.load_default(size=28)
    
    # ... (Bagian Humidity tetap sama, gunakan y_dasar=930) ...

    # --- BAGIAN UV INDEX ---
    y_uv_start = 1050
    draw.text((80, y_uv_start), "UV Index", fill="white", font=f_sedang)
    
    start_x, jarak, lebar_b, y_uv_dasar, t_max = 95, 98, 32, 1400, 150
    for i, uv in enumerate(data["uv"]):
        x1 = start_x + (i * jarak)
        # Warna UV dinamis berdasarkan indeks
        warna = (255, 200, 0) if uv > 2 else (100, 255, 150)
        y1 = y_uv_dasar - (uv * 15) # Skala UV
        draw.rounded_rectangle([x1, y1, x1 + lebar_b, y_uv_dasar], radius=16, fill=warna)
        draw.text((x1 + 16, y_uv_dasar + 30), str(uv), fill="white", font=f_kecil_b, anchor="ma")

    return kanvas

# ... (Tampilkan hasil image dan download button tetap sama) ...
