import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import io

# --- KELOLA HALAMAN WEB ---
st.set_page_config(page_title="Weather Graph App", page_icon="💧", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    iframe { background-color: transparent !important; }
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("💧 Minimalist Weather App")
st.write("Aplikasi pemantau kelembapan real-time dengan desain clean.")

if st.button("🔄 Perbarui Data Cuaca"):
    st.rerun()

# --- LOGIKA UTAMA ---
url = "https://api.open-meteo.com/v1/forecast?latitude=-6.9181&longitude=106.9266&current=temperature_2m&hourly=relative_humidity_2m&forecast_days=1"
wib = timezone(timedelta(hours=7))
jam_sekarang_obj = datetime.now(wib)

try:
    respons = requests.get(url).json()
    kelembapan_list = respons["hourly"]["relative_humidity_2m"][:10]
    waktu_list = [jam_sekarang_obj + timedelta(hours=i) for i in range(10)]
except Exception:
    kelembapan_list = [71, 69, 69, 70, 73, 77, 77, 82, 87, 90]
    waktu_list = [jam_sekarang_obj + timedelta(hours=i) for i in range(10)]

# --- LOAD FONT ---
try:
    font_SUPER_BESAR = ImageFont.truetype("Inter-Bold.ttf", 160)
    font_sedang = ImageFont.truetype("Inter-Bold.ttf", 45)
    font_kecil_bold = ImageFont.truetype("Inter-Bold.ttf", 28)
    font_kecil_regular = ImageFont.truetype("Inter-Bold.ttf", 26)
    font_header_lokasi = ImageFont.truetype("Inter-Bold.ttf", 32)
except:
    font_SUPER_BESAR = ImageFont.load_default()
    font_sedang = ImageFont.load_default()
    font_kecil_bold = ImageFont.load_default()
    font_kecil_regular = ImageFont.load_default()
    font_header_lokasi = ImageFont.load_default()

# --- GAMBAR CANVAS ---
lebar, height = 1080, 1350
kanvas = Image.new("RGBA", (lebar, height), (0, 0, 0, 0))
gambar_teks = ImageDraw.Draw(kanvas)

# Teks Header
gambar_teks.text((80, 150), "SUKABUMI REGENCY", fill=(255, 255, 255, 120), font=font_header_lokasi)

# Teks Utama
rata_rata = int(sum(kelembapan_list) / len(kelembapan_list))
gambar_teks.text((130, 322), "Humidity", fill=(255, 255, 255, 255), font=font_sedang)
gambar_teks.text((80, 400), "Today's average", fill=(255, 255, 255, 150), font=font_sedang)
gambar_teks.text((80, 470), f"{rata_rata}%", fill=(255, 255, 255, 255), font=font_SUPER_BESAR)

# Grafik Batang
layer_batang = Image.new("RGBA", (lebar, height), (0, 0, 0, 0))
gambar_batang = ImageDraw.Draw(layer_batang)
masker = Image.new("L", (lebar, height), 255)
gambar_masker = ImageDraw.Draw(masker)

start_x, jarak, lebar_batang, garis_bawah_y, tinggi_maksimal = 95, 98, 32, 930, 220

for i, persen in enumerate(kelembapan_list):
    x1 = start_x + (i * jarak)
    x2 = x1 + lebar_batang
    pusat_x = (x1 + x2) / 2
    
    tinggi_aktual = (persen / 100) * tinggi_maksimal
    y1 = garis_bawah_y - tinggi_aktual
    
    gambar_batang.rounded_rectangle([x1, y1, x2, garis_bawah_y], radius=16, fill=(240, 240, 240, 255))
    
    label_jam = "Now" if i == 0 else waktu_list[i].strftime("%H.00")
    gambar_teks.text((pusat_x, garis_bawah_y + 30), f"{persen}%", fill=(255, 255, 255, 255), font=font_kecil_bold, anchor="ma")
    gambar_teks.text((pusat_x, garis_bawah_y + 70), label_jam, fill=(255, 255, 255, 140), font=font_kecil_regular, anchor="ma")

kanvas.paste(layer_batang, (0, 0))

# Watermark
gambar_teks.text((lebar/2 - 50, 1220), "archive by", fill=(255, 255, 255, 100), font=font_kecil_regular, anchor="ma")
gambar_teks.text((lebar/2 + 60, 1220), "Andrian", fill=(255, 255, 255, 220), font=font_kecil_bold, anchor="ma")

st.image(kanvas, use_container_width=True)

# Tombol Download
buf = io.BytesIO()
kanvas.save(buf, format="PNG")
st.download_button("📥 Download Gambar PNG", data=buf.getvalue(), file_name="Grafik_Cuaca_Andrian.png", mime="image/png")
