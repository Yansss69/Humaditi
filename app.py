import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont
import io
import os

# ===============================
# CONFIG
# ===============================

st.set_page_config(
    page_title="Weather iOS",
    page_icon="🌤️",
    layout="centered"
)

st.markdown("""
<style>

.stApp{
background:#000000;
color:white;
}

header{
visibility:hidden;
}

footer{
visibility:hidden;
}

iframe{
background:transparent!important;
}

</style>
""",unsafe_allow_html=True)

st.title(" Weather iOS")

if st.button("🔄 Refresh"):
    st.rerun()

# ===============================
# LOCATION
# ===============================

LATITUDE = -6.9181
LONGITUDE = 106.9266
CITY = "SUKABUMI REGENCY"

# ===============================
# API
# ===============================

url = (
    "https://api.open-meteo.com/v1/forecast?"
    f"latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    "&current=temperature_2m,"
    "relative_humidity_2m,"
    "weather_code"
    "&hourly="
    "temperature_2m,"
    "relative_humidity_2m,"
    "uv_index,"
    "weather_code"
    "&daily="
    "sunrise,"
    "sunset"
    "&timezone=Asia%2FBangkok"
    "&forecast_days=1"
)

wib = timezone(timedelta(hours=7))
now = datetime.now(wib)

# ===============================
# GET DATA
# ===============================

try:

    data = requests.get(url, timeout=15).json()

    current_temp = round(data["current"]["temperature_2m"])

    current_humidity = round(
        data["current"]["relative_humidity_2m"]
    )

    humidity = data["hourly"]["relative_humidity_2m"][:10]

    uv = data["hourly"]["uv_index"][:10]

    temp_hour = data["hourly"]["temperature_2m"][:10]

    weather_code = data["hourly"]["weather_code"][:10]

    sunrise = data["daily"]["sunrise"][0][-5:]

    sunset = data["daily"]["sunset"][0][-5:]

except:

    current_temp = 28

    current_humidity = 74

    humidity = [74,73,71,70,69,66,63,60,58,55]

    uv = [5,5,5,4,3,2,1,0,0,0]

    temp_hour = [28,28,29,29,30,30,29,28,27,26]

    weather_code = [1]*10

    sunrise = "05:43"

    sunset = "17:56"

hours = [
    now + timedelta(hours=i)
    for i in range(10)
]

# ===============================
# IMAGE
# ===============================

WIDTH = 1080
HEIGHT = 1920

canvas = Image.new(
    "RGBA",
    (WIDTH,HEIGHT),
    (0,0,0,0)
)

draw = ImageDraw.Draw(canvas)

# ===============================
# FONT
# ===============================

def font(size):

    if os.path.exists("SF-Pro-Display-Bold.otf"):
        return ImageFont.truetype(
            "SF-Pro-Display-Bold.otf",
            size
        )

    if os.path.exists("Arial.ttf"):
        return ImageFont.truetype(
            "Arial.ttf",
            size
        )

    return ImageFont.load_default()

FONT_TITLE = font(38)
FONT_SUB = font(28)
FONT_BIG = font(150)
FONT_MED = font(56)
FONT_SMALL = font(24)
FONT_TINY = font(20)

# ===============================
# COLORS
# ===============================

WHITE = (255,255,255,255)

WHITE60 = (255,255,255,150)

WHITE30 = (255,255,255,90)

YELLOW = (255,214,10,255)

GREEN = (124,255,170,255)

ORANGE = (255,145,0,255)

RED = (255,72,72,255)

CARD = (255,255,255,18)

# ======================================================
# HEADER (iOS Weather Style)
# ======================================================

# Nama lokasi
draw.text(
    (70, 70),
    CITY,
    fill=WHITE60,
    font=FONT_SUB
)

# Menentukan deskripsi cuaca dari weather_code
def weather_text(code):
    if code == 0:
        return "Clear"
    elif code in [1, 2]:
        return "Partly Cloudy"
    elif code == 3:
        return "Cloudy"
    elif code in [45, 48]:
        return "Fog"
    elif code in [51, 53, 55]:
        return "Drizzle"
    elif code in [61, 63, 65]:
        return "Rain"
    elif code in [71, 73, 75]:
        return "Snow"
    elif code in [95, 96, 99]:
        return "Thunderstorm"
    else:
        return "Weather"

status = weather_text(weather_code[0])

# Suhu besar
draw.text(
    (70, 120),
    f"{current_temp}°",
    fill=WHITE,
    font=FONT_BIG
)

# Status cuaca
draw.text(
    (70, 300),
    status,
    fill=WHITE,
    font=FONT_MED
)

# Informasi tambahan
draw.text(
    (70, 365),
    f"Humidity {current_humidity}% • Sunrise {sunrise} • Sunset {sunset}",
    fill=WHITE60,
    font=FONT_SMALL
)

# ======================================================
# KARTU HUMIDITY (Glassmorphism)
# ======================================================

humidity_card = (
    55,
    470,
    WIDTH - 55,
    1030
)

draw.rounded_rectangle(
    humidity_card,
    radius=45,
    fill=CARD,
    outline=CARD2,
    width=2
)

# Ikon tetesan sederhana
cx = 90
cy = 520
r = 12

draw.ellipse(
    (
        cx-r,
        cy-r+6,
        cx+r,
        cy+r+6
    ),
    fill=WHITE
)

draw.polygon(
    [
        (cx, cy-20),
        (cx-r+2, cy),
        (cx+r-2, cy)
    ],
    fill=WHITE
)

draw.text(
    (120, 500),
    "Humidity",
    fill=WHITE,
    font=FONT_SUB
)

avg_humidity = round(sum(humidity)/len(humidity))

draw.text(
    (80, 570),
    "Today's average",
    fill=WHITE60,
    font=FONT_SMALL
)

draw.text(
    (80, 620),
    f"{avg_humidity}%",
    fill=WHITE,
    font=ImageFont.truetype("arial.ttf", 110) if os.path.exists("arial.ttf") else FONT_BIG
)

# Garis pemisah tipis
draw.line(
    (
        80,
        790,
        WIDTH-80,
        790
    ),
    fill=(255,255,255,40),
    width=2
)

CARD2 = (255,255,255,30)
# ======================================================
# GRAFIK HUMIDITY (iOS Style)
# ======================================================

graph_left = 90
graph_bottom = 940

bar_width = 32
spacing = 88

graph_height = 180

for i, value in enumerate(humidity):

    x = graph_left + i * spacing

    h = (value / 100) * graph_height

    y = graph_bottom - h

    # batang kapsul
    draw.rounded_rectangle(
        (
            x,
            y,
            x + bar_width,
            graph_bottom
        ),
        radius=18,
        fill=(245,245,245,255)
    )

    # lubang ala iOS
    hole_x = x + bar_width / 2
    hole_y = y + 18

    draw.ellipse(
        (
            hole_x-5,
            hole_y-5,
            hole_x+5,
            hole_y+5
        ),
        fill=(0,0,0,0)
    )

    # outline tipis supaya terlihat
    draw.ellipse(
        (
            hole_x-5,
            hole_y-5,
            hole_x+5,
            hole_y+5
        ),
        outline=(255,255,255,80),
        width=1
    )

    # nilai %
    draw.text(
        (
            x + bar_width/2,
            graph_bottom + 28
        ),
        f"{value}%",
        fill=WHITE,
        anchor="ma",
        font=FONT_TINY
    )

    # label jam
    if i == 0:
        label = "Now"
    else:
        label = hours[i].strftime("%H.00")

    draw.text(
        (
            x + bar_width/2,
            graph_bottom + 62
        ),
        label,
        fill=WHITE60,
        anchor="ma",
        font=FONT_TINY
    )

# garis bawah
draw.line(
    (
        graph_left,
        graph_bottom,
        WIDTH-90,
        graph_bottom
    ),
    fill=(255,255,255,25),
    width=2
)

# ======================================================
# FOOTNOTE
# ======================================================

draw.text(
    (
        90,
        1005
    ),
    "Humidity is the amount of water vapor present in the air.",
    fill=WHITE30,
    font=FONT_TINY
    )
# ======================================================
# UV INDEX CARD (iOS Style)
# ======================================================

card_top = 1100
card_bottom = 1620

draw.rounded_rectangle(
    (
        55,
        card_top,
        WIDTH-55,
        card_bottom
    ),
    radius=45,
    fill=CARD,
    outline=(255,255,255,35),
    width=2
)

# -----------------------------
# ICON SUN
# -----------------------------

icon_x = 90
icon_y = card_top + 45

draw.ellipse(
    (
        icon_x-10,
        icon_y-10,
        icon_x+10,
        icon_y+10
    ),
    fill=YELLOW
)

for i in range(8):

    angle = i * 45

    import math

    x1 = icon_x + math.cos(math.radians(angle))*18
    y1 = icon_y + math.sin(math.radians(angle))*18

    x2 = icon_x + math.cos(math.radians(angle))*30
    y2 = icon_y + math.sin(math.radians(angle))*30

    draw.line(
        (x1,y1,x2,y2),
        fill=YELLOW,
        width=2
    )

draw.text(
    (
        125,
        card_top+28
    ),
    "UV Index",
    fill=WHITE,
    font=FONT_SUB
)

# -----------------------------
# VALUE
# -----------------------------

current_uv = round(uv[0])

if current_uv <= 2:
    uv_text = "Low"
elif current_uv <= 5:
    uv_text = "Moderate"
elif current_uv <= 7:
    uv_text = "High"
elif current_uv <= 10:
    uv_text = "Very High"
else:
    uv_text = "Extreme"

draw.text(
    (
        80,
        card_top+95
    ),
    "Today's High",
    fill=WHITE60,
    font=FONT_SMALL
)

draw.text(
    (
        80,
        card_top+150
    ),
    f"{current_uv}",
    fill=WHITE,
    font=FONT_BIG
)

draw.text(
    (
        260,
        card_top+220
    ),
    uv_text,
    fill=WHITE,
    font=FONT_MED
)

# -----------------------------
# COLOR BAR
# -----------------------------

bar_left = 90
bar_right = WIDTH-90

bar_y = card_top+360

bar_h = 26

colors = [
    GREEN,
    GREEN,
    (220,255,100,255),
    YELLOW,
    (255,190,0,255),
    ORANGE,
    RED
]

segment = (bar_right-bar_left)//len(colors)

for i,color in enumerate(colors):

    x1 = bar_left+i*segment

    x2 = x1+segment+2

    draw.rounded_rectangle(
        (
            x1,
            bar_y,
            x2,
            bar_y+bar_h
        ),
        radius=12,
        fill=color
    )

# -----------------------------
# POINTER
# -----------------------------

pointer_x = bar_left + ((current_uv/11)*(bar_right-bar_left))

draw.ellipse(
    (
        pointer_x-12,
        bar_y-8,
        pointer_x+12,
        bar_y+34
    ),
    fill=WHITE
)

# -----------------------------
# LABELS
# -----------------------------

draw.text(
    (
        bar_left,
        bar_y+50
    ),
    "Low",
    fill=WHITE60,
    font=FONT_TINY
)

draw.text(
    (
        bar_left+210,
        bar_y+50
    ),
    "Moderate",
    fill=WHITE60,
    font=FONT_TINY
)

draw.text(
    (
        bar_left+500,
        bar_y+50
    ),
    "High",
    fill=WHITE60,
    font=FONT_TINY
)

draw.text(
    (
        90,
        card_bottom-60
    ),
    "Use sun protection from 10 AM to 4 PM when UV is Moderate or above.",
    fill=WHITE30,
    font=FONT_TINY
)
# ======================================================
# HOURLY FORECAST (iOS Style)
# ======================================================

forecast_top = 1655
forecast_bottom = 1885

draw.rounded_rectangle(
    (
        55,
        forecast_top,
        WIDTH-55,
        forecast_bottom
    ),
    radius=45,
    fill=CARD,
    outline=CARD2,
    width=2
)

draw.text(
    (
        80,
        forecast_top+25
    ),
    "Hourly Forecast",
    fill=WHITE,
    font=FONT_SUB
)

# -----------------------------
# ICON FUNCTION
# -----------------------------

def weather_icon(code):

    if code == 0:
        return "☀"

    elif code in [1,2]:
        return "⛅"

    elif code == 3:
        return "☁"

    elif code in [45,48]:
        return "🌫"

    elif code in [51,53,55]:
        return "🌦"

    elif code in [61,63,65]:
        return "🌧"

    elif code in [71,73,75]:
        return "❄"

    elif code in [95,96,99]:
        return "⛈"

    return "☀"

# -----------------------------
# DRAW FORECAST
# -----------------------------

start_x = 95
space = 95

for i in range(10):

    x = start_x + i * space

    if i == 0:
        label = "Now"
    else:
        label = hours[i].strftime("%H.00")

    draw.text(
        (x, forecast_top+70),
        label,
        fill=WHITE60,
        anchor="ma",
        font=FONT_TINY
    )

    draw.text(
        (x, forecast_top+118),
        weather_icon(weather_code[i]),
        fill=WHITE,
        anchor="ma",
        font=FONT_MED
    )

    draw.text(
        (x, forecast_top+180),
        f"{round(temp_hour[i])}°",
        fill=WHITE,
        anchor="ma",
        font=FONT_SMALL
    )

# ======================================================
# WATERMARK
# ======================================================

draw.text(
    (
        WIDTH/2,
        HEIGHT-55
    ),
    "archive by Andrian",
    fill=(255,255,255,120),
    anchor="mm",
    font=FONT_SMALL
)

# ======================================================
# SHOW IMAGE
# ======================================================

st.image(
    canvas,
    use_container_width=True
)

# ======================================================
# DOWNLOAD PNG
# ======================================================

buf = io.BytesIO()

canvas.save(
    buf,
    format="PNG"
)

st.download_button(
    "📥 Download PNG",
    buf.getvalue(),
    "Weather_iOS.png",
    "image/png"
)
