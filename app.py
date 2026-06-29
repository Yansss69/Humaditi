import streamlit as st
from PIL import Image, ImageDraw

st.set_page_config(page_title="Weather Test", layout="centered")
st.title(" Weather iOS - TEST")

# Bikin gambar polos 1080x1920
W, H = 1080, 1920
img = Image.new("RGB", (W, H), "black")
d = ImageDraw.Draw(img)

# Font bawaan PIL. Gak bakal error.
font = ImageFont.load_default() 

# Teks gede biar keliatan
d.text((100, 500), "28°", fill="white", font=font)
d.text((100, 700), "SUKABUMI", fill="gray", font=font)
d.text((100, 900), "KALAU INI MUNCUL", fill="yellow", font=font)
d.text((100, 1000), "BERARTI SCRIPT UDAH JALAN", fill="yellow", font=font)

st.image(img, use_container_width=True)
st.success("Gambar berhasil dibuat tanpa error font!")
