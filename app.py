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
st.write("Aplikasi pemantau kelembapan real-time untuk Cicurug.")

if st.button("🔄 Perbarui Data Cuaca"):
    st.rerun()

# --- LOGIKA UTAMA (Koordinat Cicurug: -6.7865, 106.7725) ---
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

# Set dimensi gambar
lebar, height = 1080, 1350
kanvas = Image.new("RGBA", (lebar, height), (0, 0, 0, 0))

# Load Font
font_SUPER_BESAR = ImageFont.load_default(size=160)
font_sedang = ImageFont.load_default(size=45)
font_kecil_bold = ImageFont.load_default(size=28)
font_kecil_regular = ImageFont.load_default(size=26)
font_header_lokasi = ImageFont.load_default(size=32)

gambar_teks = ImageDraw.Draw(kanvas)

# Teks Header Lokasi
nama_kota = "CICURUG, SUKABUMI"
gambar_teks.text((80, 150), nama_kota, fill=(255, 255, 255, 120), font=font_header_lokasi)

# Teks Utama
rata_rata = int(sum(kelembapan_list) / len(kelembapan_list))
cx, cy = 95, 345  
r_drop = 11       

gambar_teks.ellipse([cx - r_drop, cy - r_drop + 6, cx + r_drop, cy + r_drop + 6], fill=(255, 255, 255, 255))
gambar_teks.polygon([(cx, cy - 18), (cx - r_drop + 1, cy + 2), (cx + r_drop - 1, cy + 2)], fill=(255, 255, 255, 255))

gambar_teks.text((130, 322), "Humidity", fill=(255, 255, 255, 255), font=font_sedang)
gambar_teks.text((80, 400), "Today's average", fill=(255, 255, 255, 150), font=font_sedang)
gambar_teks.text((80, 470), f"{rata_rata}%", fill=(255, 255, 255, 255), font=font_SUPER_BESAR)

# Grafik Batang
layer_batang = Image.new("RGBA", (lebar, height), (0, 0, 0, 0))
gambar_batang = ImageDraw.Draw(layer_batang)
masker = Image.new("L", (lebar, height), 255)
gambar_masker = ImageDraw.Draw(masker)

start_x = 95
jarak = 98
lebar_batang = 32
garis_bawah_y = 930    
tinggi_maksimal = 220  

for i, persen in enumerate(kelembapan_list):
    x1 = start_x + (i * jarak)
    x2 = x1 + lebar_batang
    pusat_x = (x1 + x2) / 2
    
    tinggi_aktual = (persen / 100) * tinggi_maksimal
    y1 = garis_bawah_y - tinggi_aktual
    y2 = garis_bawah_y
    
    gambar_batang.rounded_rectangle([x1, y1, x2, y2], radius=16, fill=(240, 240, 240, 255))
    
    pusat_y = y1 + 16
    r = 5
    gambar_masker.ellipse([pusat_x - r, pusat_y - r, pusat_x + r, pusat_y + r], fill=0)
    
    teks_persen = f"{persen}%"
    gambar_teks.text((pusat_x, garis_bawah_y + 30), teks_persen, fill=(255, 255, 255, 255), font=font_kecil_bold, anchor="ma")
    
    label_jam = "Now" if i == 0 else waktu_list[i].strftime("%H.00")
    gambar_teks.text((pusat_x, garis_bawah_y + 70), label_jam, fill=(255, 255, 255, 140), font=font_kecil_regular, anchor="ma")

batang_berlubang = Image.new("RGBA", (lebar, height), (0, 0, 0, 0))
batang_berlubang.paste(layer_batang, (0, 0), mask=masker)
kanvas.paste(batang_berlubang, (0, 0), mask=batang_berlubang)

# Watermark
wm_x_pusat = lebar / 2
wm_y = 1220
gambar_teks.text((wm_x_pusat - 50, wm_y), "archive by", fill=(255, 255, 255, 100), font=font_kecil_regular, anchor="ma")
gambar_teks.text((wm_x_pusat + 60, wm_y), "Andrian", fill=(255, 255, 255, 220), font=font_kecil_bold, anchor="ma")

# --- MENAMPILKAN HASIL ---
st.image(kanvas, use_container_width=True)

buf = io.BytesIO()
kanvas.save(buf, format="PNG")
st.download_button(
    label="📥 Download Gambar PNG",
    data=buf.getvalue(),
    file_name="Grafik_Cuaca_Cicurug.png",
    mime="image/png"
)
