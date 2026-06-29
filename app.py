import streamlit as st
import requests
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import io
import math
import os

# ==========================================
# STREAMLIT CONFIG
# ==========================================

st.set_page_config(
    page_title="Weather iOS",
    page_icon="🌤️",
    layout="centered"
)

st.markdown("""
<style>

.stApp{
    background:#000000;
}

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

st.title(" Weather iOS")

if st.button("🔄 Refresh"):
    st.rerun()

# ==========================================
# LOCATION
# ==========================================

LATITUDE = -6.9181
LONGITUDE = 106.9266
CITY = "SUKABUMI REGENCY"

# ==========================================
# API
# ==========================================

URL = (
    "https://api.open-meteo.com/v1/forecast?"
    f"latitude={LATITUDE}"
    f"&longitude={LONGITUDE}"
    "&current=temperature_2m,relative_humidity_2m,weather_code"
    "&hourly=temperature_2m,relative_humidity_2m,uv_index,weather_code"
    "&daily=sunrise,sunset"
    "&forecast_days=1"
    "&timezone=Asia/Jakarta"
)

# ==========================================
# GET DATA
# ==========================================

try:

    response = requests.get(URL, timeout=10)

    data = response.json()

    current_temp = round(
        data["current"]["temperature_2m"]
    )

    current_humidity = round(
        data["current"]["relative_humidity_2m"]
    )

    humidity = data["hourly"]["relative_humidity_2m"][:10]

    temperature = data["hourly"]["temperature_2m"][:10]

    uv = data["hourly"]["uv_index"][:10]

    weather = data["hourly"]["weather_code"][:10]

    sunrise = data["daily"]["sunrise"][0][-5:]

    sunset = data["daily"]["sunset"][0][-5:]

except Exception:

    current_temp = 28
    current_humidity = 73

    humidity = [73,72,71,70,68,65,61,58,56,54]

    temperature = [28,28,29,29,30,30,29,28,27,26]

    uv = [5,5,5,4,3,2,1,0,0,0]

    weather = [1]*10

    sunrise = "05:43"

    sunset = "17:56"

# ==========================================
# TIME
# ==========================================

now = datetime.now()

hours = [
    now + timedelta(hours=i)
    for i in range(10)
]

# ==========================================
# CANVAS
# ==========================================

WIDTH = 1080
HEIGHT = 1920

canvas = Image.new(
    "RGBA",
    (WIDTH, HEIGHT),
    (0,0,0,0)
)

draw = ImageDraw.Draw(canvas)

# ==========================================
# FONT
# ==========================================

def load_font(size):

    fonts = [
        "SF-Pro-Display-Regular.otf",
        "SFProDisplay-Regular.otf",
        "DejaVuSans.ttf",
        "arial.ttf"
    ]

    for f in fonts:

        try:
            return ImageFont.truetype(f, size)

        except:

            pass

    return ImageFont.load_default()

FONT_BIG = load_font(170)
FONT_TITLE = load_font(56)
FONT_SUB = load_font(34)
FONT_SMALL = load_font(26)
FONT_TINY = load_font(22)

# ==========================================
# COLORS
# ==========================================

WHITE = (255,255,255,255)

WHITE80 = (255,255,255,200)

WHITE60 = (255,255,255,150)

WHITE40 = (255,255,255,100)

WHITE20 = (255,255,255,40)

CARD = (255,255,255,18)

CARD_BORDER = (255,255,255,35)

GREEN = (119,255,170,255)

YELLOW = (255,214,10,255)

ORANGE = (255,150,0,255)

RED = (255,60,60,255)

# ==========================================
# WEATHER TEXT
# ==========================================

def weather_text(code):

    if code == 0:
        return "Clear"

    elif code in [1,2]:
        return "Partly Cloudy"

    elif code == 3:
        return "Cloudy"

    elif code in [45,48]:
        return "Fog"

    elif code in [51,53,55]:
        return "Drizzle"

    elif code in [61,63,65]:
        return "Rain"

    elif code in [71,73,75]:
        return "Snow"

    elif code in [95,96,99]:
        return "Thunderstorm"

    return "Weather"

status = weather_text(weather[0])
# ==========================================
# HEADER
# ==========================================

# Lokasi
draw.text(
    (70, 80),
    CITY,
    fill=WHITE60,
    font=FONT_SUB
)

# Suhu besar
draw.text(
    (70, 120),
    f"{current_temp}°",
    fill=WHITE,
    font=FONT_BIG
)

# Status cuaca
draw.text(
    (70, 305),
    status,
    fill=WHITE80,
    font=FONT_TITLE
)

# Detail
draw.text(
    (70, 365),
    f"Humidity {current_humidity}%    Sunrise {sunrise}    Sunset {sunset}",
    fill=WHITE60,
    font=FONT_SMALL
)

# ==========================================
# HUMIDITY CARD
# ==========================================

humidity_card = (
    50,
    450,
    WIDTH-50,
    1050
)

draw.rounded_rectangle(
    humidity_card,
    radius=40,
    fill=CARD,
    outline=CARD_BORDER,
    width=2
)

# Icon tetesan

cx = 90
cy = 510

draw.ellipse(
    (
        cx-10,
        cy,
        cx+10,
        cy+20
    ),
    fill=WHITE
)

draw.polygon(
    (
        (cx, cy-18),
        (cx-10, cy+5),
        (cx+10, cy+5)
    ),
    fill=WHITE
)

draw.text(
    (120,490),
    "Humidity",
    fill=WHITE,
    font=FONT_SUB
)

avg_humidity = round(sum(humidity)/len(humidity))

draw.text(
    (80,560),
    "Today's average",
    fill=WHITE60,
    font=FONT_SMALL
)

draw.text(
    (80,610),
    f"{avg_humidity}%",
    fill=WHITE,
    font=load_font(120)
)

# garis tipis

draw.line(
    (
        80,
        785,
        WIDTH-80,
        785
    ),
    fill=WHITE20,
    width=2
)

# ==========================================
# HUMIDITY GRAPH
# ==========================================

graph_left = 90
graph_bottom = 940

bar_width = 34
spacing = 88
max_height = 140

for i, value in enumerate(humidity):

    x = graph_left + i * spacing

    h = (value / 100) * max_height

    y = graph_bottom - h

    draw.rounded_rectangle(
        (
            x,
            y,
            x+bar_width,
            graph_bottom
        ),
        radius=18,
        fill=(245,245,245,255)
    )

    # lubang iOS

    hole_x = x + bar_width/2
    hole_y = y + 18

    draw.ellipse(
        (
            hole_x-4,
            hole_y-4,
            hole_x+4,
            hole_y+4
        ),
        fill=(0,0,0,0)
    )

    draw.text(
        (
            x+bar_width/2,
            graph_bottom+30
        ),
        f"{value}%",
        anchor="ma",
        fill=WHITE,
        font=FONT_TINY
    )

    if i == 0:
        jam = "Now"
    else:
        jam = hours[i].strftime("%H.00")

    draw.text(
        (
            x+bar_width/2,
            graph_bottom+62
        ),
        jam,
        anchor="ma",
        fill=WHITE60,
        font=FONT_TINY
    )

draw.text(
    (
        90,
        1010
    ),
    "Humidity is the amount of water vapor currently present in the air.",
    fill=WHITE40,
    font=FONT_TINY
)
# ==========================================
# UV INDEX CARD
# ==========================================

uv_card = (
    50,
    1080,
    WIDTH-50,
    1600
)

draw.rounded_rectangle(
    uv_card,
    radius=40,
    fill=CARD,
    outline=CARD_BORDER,
    width=2
)

# ----------------------------
# Icon Matahari
# ----------------------------

sun_x = 90
sun_y = 1135

draw.ellipse(
    (
        sun_x-10,
        sun_y-10,
        sun_x+10,
        sun_y+10
    ),
    fill=YELLOW
)

for angle in range(0,360,45):

    x1 = sun_x + math.cos(math.radians(angle))*18
    y1 = sun_y + math.sin(math.radians(angle))*18

    x2 = sun_x + math.cos(math.radians(angle))*30
    y2 = sun_y + math.sin(math.radians(angle))*30

    draw.line(
        (x1,y1,x2,y2),
        fill=YELLOW,
        width=2
    )

draw.text(
    (120,1115),
    "UV Index",
    fill=WHITE,
    font=FONT_SUB
)

# ----------------------------
# UV VALUE
# ----------------------------

current_uv = round(uv[0])

if current_uv <= 2:
    uv_status = "Low"
elif current_uv <= 5:
    uv_status = "Moderate"
elif current_uv <= 7:
    uv_status = "High"
elif current_uv <= 10:
    uv_status = "Very High"
else:
    uv_status = "Extreme"

draw.text(
    (80,1185),
    "Today's High",
    fill=WHITE60,
    font=FONT_SMALL
)

draw.text(
    (80,1235),
    str(current_uv),
    fill=WHITE,
    font=load_font(120)
)

draw.text(
    (220,1290),
    uv_status,
    fill=WHITE,
    font=FONT_TITLE
)

# ----------------------------
# UV BAR
# ----------------------------

bar_left = 90
bar_top = 1410
bar_width = 850
bar_height = 22

colors = [
    GREEN,
    (180,255,120,255),
    YELLOW,
    (255,180,0,255),
    ORANGE,
    RED
]

segment = bar_width / len(colors)

for i, color in enumerate(colors):

    x1 = bar_left + i*segment

    x2 = x1 + segment

    draw.rounded_rectangle(
        (
            x1,
            bar_top,
            x2,
            bar_top+bar_height
        ),
        radius=10,
        fill=color
    )

# ----------------------------
# POINTER
# ----------------------------

pointer = bar_left + (current_uv/11)*bar_width

draw.ellipse(
    (
        pointer-8,
        bar_top-8,
        pointer+8,
        bar_top+30
    ),
    fill=WHITE
)

# ----------------------------
# LABEL
# ----------------------------

draw.text(
    (90,1470),
    "Low",
    fill=WHITE60,
    font=FONT_TINY
)

draw.text(
    (340,1470),
    "Moderate",
    fill=WHITE60,
    font=FONT_TINY
)

draw.text(
    (650,1470),
    "High",
    fill=WHITE60,
    font=FONT_TINY
)

draw.text(
    (
        90,
        1535
    ),
    "Protection is recommended when UV Index is Moderate or above.",
    fill=WHITE40,
    font=FONT_TINY
)
# ==========================================
# HOURLY FORECAST CARD
# ==========================================

forecast_card = (
    50,
    1630,
    WIDTH-50,
    1910
)

draw.rounded_rectangle(
    forecast_card,
    radius=40,
    fill=CARD,
    outline=CARD_BORDER,
    width=2
)

draw.text(
    (80,1660),
    "Hourly Forecast",
    fill=WHITE,
    font=FONT_SUB
)

# ==========================================
# SIMPLE WEATHER ICON
# ==========================================

def draw_weather_icon(x, y, code):

    # Matahari
    if code == 0:

        draw.ellipse(
            (x-10, y-10, x+10, y+10),
            fill=YELLOW
        )

        for ang in range(0,360,45):

            x1 = x + math.cos(math.radians(ang))*14
            y1 = y + math.sin(math.radians(ang))*14

            x2 = x + math.cos(math.radians(ang))*22
            y2 = y + math.sin(math.radians(ang))*22

            draw.line(
                (x1,y1,x2,y2),
                fill=YELLOW,
                width=2
            )

    # Berawan
    else:

        draw.ellipse(
            (x-16,y-6,x+2,y+12),
            fill=WHITE
        )

        draw.ellipse(
            (x-2,y-12,x+18,y+10),
            fill=WHITE
        )

        draw.rectangle(
            (x-16,y,x+18,y+12),
            fill=WHITE
        )

# ==========================================
# DRAW FORECAST
# ==========================================

start_x = 95
spacing = 95

for i in range(10):

    x = start_x + i * spacing

    if i == 0:
        label = "Now"
    else:
        label = hours[i].strftime("%H.%M")

    draw.text(
        (x,1710),
        label,
        fill=WHITE60,
        font=FONT_TINY,
        anchor="ma"
    )

    draw_weather_icon(
        x,
        1765,
        weather[i]
    )

    draw.text(
        (x,1820),
        f"{round(temperature[i])}°",
        fill=WHITE,
        font=FONT_SMALL,
        anchor="ma"
    )

# ==========================================
# FOOTER
# ==========================================

draw.text(
    (WIDTH/2, HEIGHT-25),
    "archive by Andrian",
    fill=WHITE40,
    font=FONT_SMALL,
    anchor="ms"
)

# ==========================================
# SHOW IMAGE
# ==========================================

st.image(
    canvas,
    use_container_width=True
)

# ==========================================
# DOWNLOAD
# ==========================================

buffer = io.BytesIO()

canvas.save(
    buffer,
    format="PNG"
)

st.download_button(
    "📥 Download PNG",
    data=buffer.getvalue(),
    file_name="weather_ios.png",
    mime="image/png"
)
