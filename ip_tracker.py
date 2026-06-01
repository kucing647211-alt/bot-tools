import requests

def cek_ip(ip=None):
    """Cek info IP address. Kalau ip=None, cek IP user sendiri."""
    try:
        if ip:
            url = f"http://ip-api.com/json/{ip}?lang=id"
        else:
            url = "http://ip-api.com/json/?lang=id"

        r = requests.get(url, timeout=10)
        data = r.json()

        if data.get("status") == "fail":
            return None

        return {
            "ip": data.get("query", "?"),
            "negara": data.get("country", "?"),
            "kode_negara": data.get("countryCode", "?"),
            "wilayah": data.get("regionName", "?"),
            "kota": data.get("city", "?"),
            "kodepos": data.get("zip", "?"),
            "isp": data.get("isp", "?"),
            "org": data.get("org", "?"),
            "timezone": data.get("timezone", "?"),
            "lat": data.get("lat", 0),
            "lon": data.get("lon", 0),
            "mobile": data.get("mobile", False),
            "proxy": data.get("proxy", False),
            "hosting": data.get("hosting", False),
        }
    except Exception as e:
        return None

def format_hasil(data):
    """Format hasil IP tracker jadi teks Telegram"""
    proxy_status = "⚠️ Ya" if data["proxy"] else "✅ Tidak"
    mobile_status = "📱 Ya" if data["mobile"] else "💻 Tidak"
    hosting_status = "🖥️ Ya (VPS/Server)" if data["hosting"] else "🏠 Tidak"
    maps_link = f"https://maps.google.com/?q={data['lat']},{data['lon']}"

    return (
        f"📍 *Hasil IP Tracker*\n\n"
        f"🌐 *IP:* `{data['ip']}`\n"
        f"🏳️ *Negara:* {data['negara']} ({data['kode_negara']})\n"
        f"🏙️ *Kota:* {data['kota']}, {data['wilayah']}\n"
        f"📮 *Kodepos:* {data['kodepos']}\n"
        f"📡 *ISP:* {data['isp']}\n"
        f"🏢 *Organisasi:* {data['org']}\n"
        f"🕐 *Timezone:* {data['timezone']}\n"
        f"📍 *Koordinat:* `{data['lat']}, {data['lon']}`\n"
        f"🗺️ *Maps:* [Lihat di Google Maps]({maps_link})\n\n"
        f"🔒 *Proxy/VPN:* {proxy_status}\n"
        f"📱 *Mobile:* {mobile_status}\n"
        f"🖥️ *Hosting:* {hosting_status}"
    )
