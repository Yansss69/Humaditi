import streamlit as st
from PIL import Image, ImageDraw, ImageFont # <-- INI YANG KURANG TADI

st.set_page_config(page_title="Weather Test", layout="centered")
st.title(" Weather iOS - TEST FIXED")

W, H = 1080, 1920
img = Image.new("RGB", (W, H), "black")
d = ImageDraw.Draw(img)

font = ImageFont.load_default() # Sekarang udah ke-import, gak error lagi

d.text((100, 500), "28°", fill="white", font=font)
d.text((100, 700), "SUKABUMI", fill="gray", font=font)
d.text((100, 900), "UDAH JALAN NIH", fill="lime", font=font)
d.text((100, 1000), "MAAF TADI LUPA IMPORT", fill="lime", font=font)

st.image(img, use_container_width=True)
st.success("Gak ada error font lagi!")
