import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="Weather iOS", layout="centered")
st.title(" Weather iOS")

W, H = 1080, 1920
img = Image.new("RGB", (W, H), "black")
d = ImageDraw.Draw(img)

# KUNCI: Load font dari file .ttf yang kita upload
font_path = "Inter-Bold.ttf" 
try:
    FONT_BIG = ImageFont.truetype(font_path, 180) # Suhu gede
    FONT_SUB = ImageFont.truetype(font_path, 42)  # Kota
    FONT_SMALL = ImageFont.truetype(font_path, 28) # Keterangan
except:
    st.error(f"File {font_path} gak ketemu. Upload ke GitHub ya.")
    st.stop()

# Gambar
d.text((70, 120), "28°", fill="white", font=FONT_BIG)
d.text((70, 330), "SUKABUMI REGENCY", fill=(255,255,255,150), font=FONT_SUB)
d.text((70, 400), "Partly Cloudy  Humidity 73%", fill=(255,255,255,150), font=FONT_SMALL)
d.text((70, 1700), "Udah Gede & Gak Error", fill="lime", font=FONT_SUB)

st.image(img, use_container_width=True)
