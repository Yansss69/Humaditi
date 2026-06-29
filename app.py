url = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude=-6.9181"
    "&longitude=106.9266"
    "&current=temperature_2m"
    "&hourly=relative_humidity_2m,uv_index"
    "&forecast_days=1"
)
try:
    respons = requests.get(url).json()

    kelembapan_list = respons["hourly"]["relative_humidity_2m"][:10]
    uv_list = respons["hourly"]["uv_index"][:10]

    waktu_list = [
        jam_sekarang_obj + timedelta(hours=i)
        for i in range(10)
    ]

except:
    kelembapan_list = [71,69,69,70,73,77,77,82,87,90]
    uv_list = [5,5,5,3,2,0,0,0,0,0]

    waktu_list = [
        jam_sekarang_obj + timedelta(hours=i)
        for i in range(10)
    ]
    uv_max = max(uv_list)

if uv_max <= 2:
    kategori = "Low"
elif uv_max <= 5:
    kategori = "Moderate"
elif uv_max <= 7:
    kategori = "High"
elif uv_max <= 10:
    kategori = "Very High"
else:
    kategori = "Extreme"

gambar_teks.text(
    (80,720),
    "☀ UV Index",
    fill=(255,255,255,255),
    font=font_sedang
)

gambar_teks.text(
    (80,780),
    "Today's high",
    fill=(255,255,255,140),
    font=font_kecil_regular
)

gambar_teks.text(
    (80,840),
    f"{uv_max} {kategori}",
    fill=(255,255,255,255),
    font=font_SUPER_BESAR
)
uv_start_y = 1180
uv_bar_height = 120

for i, uv in enumerate(uv_list):

    x = start_x + i * jarak

    if uv >= 8:
        warna = (255,80,80,255)
    elif uv >= 6:
        warna = (255,165,0,255)
    elif uv >= 3:
        warna = (255,210,70,255)
    elif uv > 0:
        warna = (120,255,180,255)
    else:
        warna = (90,180,120,180)

    tinggi = max(10, uv * 18)

    gambar_teks.rounded_rectangle(
        (
            x,
            uv_start_y - tinggi,
            x + 38,
            uv_start_y
        ),
        radius=20,
        fill=warna
    )

    gambar_teks.text(
        (x+19, uv_start_y+25),
        str(int(uv)),
        fill=(255,255,255),
        anchor="ma",
        font=font_kecil_bold
    )
    # Hijau
(120,255,170,255)

# Kuning
(255,212,65,255)

# Orange
(255,145,0,255)

# Merah
(255,70,70,255)
    
