import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Twitter/X": "https://twitter.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Telegram": "https://t.me/{}",
    "Medium": "https://medium.com/@{}",
    "Dev.to": "https://dev.to/{}",
    "Replit": "https://replit.com/@{}",
    "Linktree": "https://linktr.ee/{}",
    "Patreon": "https://www.patreon.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
}

def cek_username(username):
    """Cek username di berbagai platform"""
    hasil = {}
    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username)
        try:
            r = requests.get(url, headers=HEADERS, timeout=6, allow_redirects=True)
            if r.status_code == 200:
                hasil[platform] = {"status": "ADA", "url": url}
            elif r.status_code == 404:
                hasil[platform] = {"status": "KOSONG", "url": url}
            else:
                hasil[platform] = {"status": "TIDAK DIKETAHUI", "url": url}
        except:
            hasil[platform] = {"status": "ERROR", "url": url}
    return hasil

def format_hasil(username, hasil):
    ada = [(p, d["url"]) for p, d in hasil.items() if d["status"] == "ADA"]
    kosong = [p for p, d in hasil.items() if d["status"] == "KOSONG"]
    error = [p for p, d in hasil.items() if d["status"] in ("ERROR", "TIDAK DIKETAHUI")]

    teks = f"🔍 *Hasil Cek Username:* `{username}`\n\n"

    if ada:
        teks += f"✅ *Ditemukan di {len(ada)} platform:*\n"
        for platform, url in ada:
            teks += f"• [{platform}]({url})\n"
        teks += "\n"

    if kosong:
        teks += f"⭕ *Tersedia di {len(kosong)} platform:*\n"
        for platform in kosong:
            teks += f"• {platform}\n"
        teks += "\n"

    if error:
        teks += f"❓ *Tidak bisa dicek ({len(error)}):*\n"
        for platform in error:
            teks += f"• {platform}\n"

    return teks
