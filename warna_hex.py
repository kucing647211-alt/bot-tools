import re

def hex_ke_rgb(hex_color):
    """Convert hex color ke RGB"""
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    if len(hex_color) != 6:
        return None
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return {"r": r, "g": g, "b": b, "hex": f"#{hex_color.upper()}"}
    except:
        return None

def rgb_ke_hex(r, g, b):
    """Convert RGB ke hex color"""
    try:
        r, g, b = int(r), int(g), int(b)
        if not all(0 <= x <= 255 for x in [r, g, b]):
            return None
        hex_color = f"#{r:02X}{g:02X}{b:02X}"
        return {"r": r, "g": g, "b": b, "hex": hex_color}
    except:
        return None

def nama_warna_approx(r, g, b):
    """Tebak nama warna berdasarkan RGB"""
    warna = [
        ((255, 0, 0), "Merah"),
        ((0, 255, 0), "Hijau"),
        ((0, 0, 255), "Biru"),
        ((255, 255, 0), "Kuning"),
        ((255, 165, 0), "Oranye"),
        ((128, 0, 128), "Ungu"),
        ((255, 192, 203), "Pink"),
        ((165, 42, 42), "Coklat"),
        ((0, 0, 0), "Hitam"),
        ((255, 255, 255), "Putih"),
        ((128, 128, 128), "Abu-abu"),
        ((0, 255, 255), "Cyan"),
        ((255, 0, 255), "Magenta"),
        ((0, 128, 128), "Teal"),
        ((255, 215, 0), "Emas"),
    ]
    jarak_min = float('inf')
    nama = "Tidak diketahui"
    for (wr, wg, wb), nama_w in warna:
        jarak = ((r-wr)**2 + (g-wg)**2 + (b-wb)**2) ** 0.5
        if jarak < jarak_min:
            jarak_min = jarak
            nama = nama_w
    return nama

def hsl_dari_rgb(r, g, b):
    """Hitung nilai HSL dari RGB"""
    r_, g_, b_ = r/255, g/255, b/255
    cmax = max(r_, g_, b_)
    cmin = min(r_, g_, b_)
    delta = cmax - cmin
    l = (cmax + cmin) / 2

    if delta == 0:
        h = s = 0
    else:
        s = delta / (1 - abs(2*l - 1))
        if cmax == r_:
            h = 60 * (((g_ - b_) / delta) % 6)
        elif cmax == g_:
            h = 60 * (((b_ - r_) / delta) + 2)
        else:
            h = 60 * (((r_ - g_) / delta) + 4)

    return round(h), round(s * 100), round(l * 100)

def format_hasil(data):
    r, g, b = data["r"], data["g"], data["b"]
    nama = nama_warna_approx(r, g, b)
    h, s, l = hsl_dari_rgb(r, g, b)
    return (
        f"🌈 *Konverter Warna*\n\n"
        f"🎨 *Warna:* {nama}\n\n"
        f"🔢 *HEX:* `{data['hex']}`\n"
        f"🔴 *RGB:* `rgb({r}, {g}, {b})`\n"
        f"🌀 *HSL:* `hsl({h}°, {s}%, {l}%)`\n\n"
        f"📋 *CSS siap pakai:*\n"
        f"`color: {data['hex']};`\n"
        f"`background: rgb({r}, {g}, {b});`"
    )

def parse_input(teks):
    """Parse input user, bisa hex atau rgb"""
    teks = teks.strip()
    # Cek format hex
    if re.match(r'^#?[0-9A-Fa-f]{3}(?:[0-9A-Fa-f]{3})?$', teks):
        return "hex", teks
    # Cek format rgb(r, g, b)
    rgb_match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', teks, re.IGNORECASE)
    if rgb_match:
        return "rgb", (int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3)))
    # Cek format r,g,b langsung
    parts = re.split(r'[,\s]+', teks)
    if len(parts) == 3 and all(p.isdigit() for p in parts):
        return "rgb", (int(parts[0]), int(parts[1]), int(parts[2]))
    return None, None
