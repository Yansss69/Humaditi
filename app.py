import streamlit as st
import requests
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import io
import math

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="Weather iOS", page_icon="🌤️", layout="centered")
st.markdown("""<style>.stApp{background:#000;} header,footer{visibility:hidden;}</style>""", unsafe_allow_html=True)
st.title(" Weather iOS")
if st.button("🔄 Refresh"): st.rerun()

LAT, LON, CITY = -6.9181, 106.9266, "SUKABUMI REGENCY"
W, H = 1080, 1920

# Warna
W, W80, W60, W40 = (255,255,255), (255,255,255,200), (255,255,255,150), (255,255,255,100)
CARD, BORDER = (255,255,255,18), (255,255,255,35)
G, Y, O, R = (119,255,170), (255,214,10), (255,150,0), (255,60,60)

# ==========================================
# FONT ANTI ERROR 100% - PAKAI DEFAULT DOANG
# ==========================================
@st.cache_resource
def get_fonts():
    # load_default() gak bakal error di server manapun
    base = ImageFont.load_default()
    # Trik: scale font biar keliatan gede. 5.0 = paling gede
    return {
        "big": base.font_variant(size=180), # Suhu
        "big2": base.font_variant(size=120), # Angka UV/Hum
        "title": base.font_variant(size=60), # Status
        "sub": base.font_variant(size=36), # Judul Card
        "small": base.font_variant(size=28), # Detail
        "med": base.font_variant(size=24), # Temp Forecast
        "tiny": base.font_variant(size=20), # Label
    }
F = get_fonts()

# ==========================================
# DATA
# ==========================================
@st.cache_data(ttl=600)
def get_data():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,weather_code&hourly=temperature_2m,uv_index,weather_code&daily=sunrise,sunset&forecast_days=1&timezone=Asia/Jakarta"
        d = requests.get(url, timeout=5).json()
        return {"t":round(d["current"]["temperature_2m"]), "h":round(d["current"]["relative_humidity_2m"]), "hh":d["hourly"]["relative_humidity_2m"][:10], "th":d["hourly"]["temperature_2m"][:10], "uv":d["hourly"]["uv_index"][:10], "wc":d["hourly"]["weather_code"][:10], "sr":d["daily"]["sunrise"][0][-5:], "ss":d["daily"]["sunset"][0][-5:]}
    except:
        return {"t":28,"h":73,"hh":[73,72,71,70,68,65,61,58,56,54],"th":[28,28,29,29,30,30,29,28,27,26],"uv":[5,5,5,4,3,2,1,0,0,0],"wc":[1]*10,"sr":"05:43","ss":"17:56"}

D = get_data()
HOURS = [datetime.now() + timedelta(hours=i) for i in range(10)]

# ==========================================
# HELPER
# ==========================================
def w_text(c): return {0:"Clear",1:"Partly Cloudy",2:"Partly Cloudy",3:"Cloudy"}.get(c, "Cloudy")
def uv_stat(v): return ("Low",G) if v<=2 else ("Moderate",Y) if v<=5 else ("High",O) if v<=7 else ("Very High",R) if v<=10 else ("Extreme",(128,0,128))

def icon(draw,x,y,c,s=20):
    if c==0: draw.ellipse((x-s,y-s,x+s,y+s),fill=Y); [draw.line((x+math.cos(math.radians(a))*(s+4),y+math.sin(math.radians(a))*(s+4),x+math.cos(math.radians(a))*(s+12),y+math.sin(math.radians(a))*(s+12)),fill=Y,width=3) for a in range(0,360,45)]
    else: draw.ellipse((x-s,y-s//2,x+s//4,y+s//2),fill=W); draw.ellipse((x-s//4,y-s,x+s,y+s//2),fill=W); draw.rectangle((x-s,y,x+s,y+s//2),fill=W)

# ==========================================
# DRAW
# ==========================================
IMG = Image.new("RGB",(W,H),(0,0,0)); DRA = ImageDraw.Draw(IMG)

# HEADER
DRA.text((70,80),CITY,fill=W60,font=F["sub"]); DRA.text((70,120),f"{D['t']}°",fill=W,font=F["big"])
DRA.text((70,330),w_text(D['wc'][0]),fill=W80,font=F["title"]); DRA.text((70,400),f"Humidity {D['h']}% Sunrise {D['sr']} Sunset {D['ss']}",fill=W60,font=F["small"])

# CARD HUMIDITY
DRA.rounded_rectangle((50,470,W-50,1070),40,fill=CARD,outline=BORDER,width=2)
DRA.ellipse((78,530,102,552),fill=W); DRA.polygon(((90,510),(78,536),(102,536)),fill=W)
DRA.text((130,510),"Humidity",fill=W,font=F["sub"]); DRA.text((80,580),"Today's average",fill=W60,font=F["small"])
DRA.text((80,630),f"{round(sum(D['hh'])/10)}%",fill=W,font=F["big2"]); DRA.line((80,800,W-80,800),fill=W40,width=2)

# BAR HUM
gl,gb,bw,sp,mh = 90,950,40,92,160
for i,v in enumerate(D['hh']): x=gl+i*sp; y=gb-(v/100)*mh; DRA.rounded_rectangle((x,y,x+bw,gb),20,fill=(245,245,245)); DRA.text((x+bw/2,gb+35),f"{v}%",anchor="ma",fill=W,font=F["tiny"]); DRA.text((x+bw/2,gb+70),"Now" if i==0 else HOURS[i].strftime("%H:00"),anchor="ma",fill=W60,font=F["tiny"])

# CARD UV
DRA.rounded_rectangle((50,1100,W-50,1620),40,fill=CARD,outline=BORDER,width=2)
sx,sy=90,1155; DRA.ellipse((sx-12,sy-12,sx+12,sy+12),fill=Y); [DRA.line((sx+math.cos(math.radians(a))*20,sy+math.sin(math.radians(a))*20,sx+math.cos(math.radians(a))*32,sy+math.sin(math.radians(a))*32),fill=Y,width=3) for a in range(0,360,45)]
DRA.text((130,1135),"UV Index",fill=W,font=F["sub"]); UV=round(D['uv'][0]); ST,SC=uv_stat(UV)
DRA.text((80,1230),"Today's High",fill=W60,font=F["small"]); DRA.text((80,1280),str(UV),fill=W,font=F["big2"]); DRA.text((240,1340),ST,fill=SC,font=F["title"])

# BAR UV
bl,bt,bw,bh=90,1440,850,26; CS=[G,(180,255,120),Y,(255,180,0),O,R]; SG=bw/len(CS)
for i,c in enumerate(CS): DRA.rounded_rectangle((bl+i*SG,bt,bl+(i+1)*SG,bt+bh),12,fill=c)
PT=bl+(UV/11)*bw; DRA.ellipse((PT-10,bt-10,PT+10,bt+bh+10),fill=W,outline=(0,0,0,80),width=3)
DRA.text((90,1500),"Low",fill=W60,font=F["tiny"]); DRA.text((350,1500),"Moderate",fill=W60,font=F["tiny"]); DRA.text((680,1500),"High",fill=W60,font=F["tiny"])

# FORECAST
DRA.rounded_rectangle((50,1650,W-50,H-50),40,fill=CARD,outline=BORDER,width=2); DRA.text((80,168
