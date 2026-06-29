import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import io

# Fungsi untuk memuat font yang lebih baik (pastikan ada file font di folder Anda)
def get_font(size):
    try:
        # Gunakan font bawaan jika ada, atau ganti dengan nama file font .ttf yang Anda unggah
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

def create_weather_image(data):
    lebar, tinggi = 1080, 1600
    kanvas = Image.new("RGBA", (lebar, tinggi), (0, 0, 0, 0))
    draw = ImageDraw.Draw(kanvas)
    
    # Font kustom untuk estetika yang lebih baik
    f_header = get_font(40)
    f_teks = get_font(30)
    
    # Judul
    draw.text((80, 100), "SUKABUMI REGENCY", fill="white", font=f_header)
    
    # Menggambar Humidity (Posisi lebih rapi)
    start_x, jarak = 95, 98
    for i, h in enumerate(data["humidity"]):
        # Bar dibuat lebih proporsional
        x = start_x + (i * jarak)
        draw.rounded_rectangle([x, 200, x + 50, 500], radius=20, fill=(255, 255, 255, 255))
        draw.text((x + 25, 530), f"{h}%", fill="white", font=f_teks, anchor="ma")

    # Menggambar UV (Posisi disesuaikan agar tidak menempel)
    draw.text((80, 700), "UV Index", fill="white", font=f_header)
    for i, uv in enumerate(data["uv"]):
        x = start_x + (i * jarak)
        warna = (255, 200, 0) if uv > 2 else (100, 255, 150)
        draw.rounded_rectangle([x, 800, x + 50, 1100], radius=20, fill=warna)
        draw.text((x + 25, 1130), str(int(uv)), fill="white", font=f_teks, anchor="ma")
    
    return kanvas

# ... (bagian pemanggilan fungsi dan tampilan web sama seperti sebelumnya)
