import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import io
import os

# --- KELOLA HALAMAN WEB ---
st.set_page_config(page_title="Weather Graph App", page_icon="💧", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("💧 Minimalist Weather App")
st.write("Aplikasi pemantau kelembapan real-time untuk Cicurug.")

if st.button("🔄 Perbarui Data Cuaca"):
    st.rerun()

# --- LOGIKA DATA (Cicurug: -6.7865, 106.7725) ---
url = "https://api.open-meteo.com/v1/forecast?latitude=-6.7865&longitude=106.7725&current=temperature_2m&hourly=relative_humidity_2m&forecast_days=1"
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
font_path = "Inter-Bold.ttf"
if os.path.exists(font_path):
    font_SUPER_BESAR = ImageFont.truetype(font_path, 160)
    font_sedang = ImageFont.truetype(font_path, 45)
    font_kecil_bold = ImageFont.truetype(font_path, 28)
    font_kecil_regular = ImageFont.truetype(font_path, 26)
    font_header_lokasi = ImageFont.truetype(font_path, 32)
else:
    st.warning("File font 'Inter-Bold.ttf' tidak ditemukan, menggunakan font default.")
    font_SUPER_BESAR = ImageFont.load_default()
    font_sedang = ImageFont.load_default()
    font_kecil_bold = ImageFont.load_default()
    font_kecil_regular = ImageFont.load_default()
    font_header_lokasi = ImageFont.load_default()

# --- RENDER GAMBAR ---
lebar, height = 1080, 1350
kanvas = Image.new("RGBA", (lebar, height), (0, 0, 0, 0))
gambar_teks = ImageDraw.Draw(kanvas)

# Header
gambar_teks.text((80, 150), "CICURUG, SUKABUMI", fill=(255, 255, 255, 120), font=font_header_lokasi)

# Statistik Utama
rata_rata = int(sum(kelembapan_list) / len(kelembapan_list))
gambar_teks.text((130, 322), "Humidity", fill=(255, 255, 255, 255), font=font_sedang)
gambar_teks.text((80, 400), "Today's average", fill=(255, 255, 255, 150), font=font_sedang)
gambar_teks.text((80, 470), f"{rata_rata}%", fill=(255, 255, 255, 255), font=font_SUPER_BESAR)

# Grafik
layer_batang = Image.new("RGBA", (lebar, height), (0, 0, 0, 0))
gambar_batang = ImageDraw.Draw(layer_batang)
masker = Image.new("L", (lebar, height), 255)
gambar_masker = ImageDraw.Draw(masker)

start_x, jarak, lebar_batang, garis_bawah_y, tinggi_maksimal = 95, 98, 32, 930, 220

for i, persen in enumerate(kelembapan_list):
    x1 = start_x + (i * jarak)
    x2 = x1 + lebar_batang
    y1 = garis_bawah_y - ((persen / 100) * tinggi_maksimal)
    
    gambar_batang.rounded_rectangle([x1, y1, x2, garis_bawah_y], radius=16, fill=(240, 240, 240, 255))
    
    label_jam = "Now" if i == 0 else waktu_list[i].strftime("%H.00")
    gambar_teks.text(((x1 + x2) / 2, garis_bawah_y + 30), f"{persen}%", fill=(255, 255, 255, 255), font=font_kecil_bold, anchor="ma")
    gambar_teks.text(((x1 + x2) / 2, garis_bawah_y + 70), label_jam, fill=(255, 255, 255, 140), font=font_kecil_regular, anchor="ma")

kanvas.paste(layer_batang, (0, 0), mask=masker)

# Footer
gambar_teks.text((lebar/2 - 50, 1220), "archive by", fill=(255, 255, 255, 100), font=font_kecil_regular, anchor="ma")
