import requests

def simpan_pastebin(teks, judul="Untitled", ekspirasi=3600):
    """Simpan teks ke dpaste.org (gratis, tanpa API key)"""
    try:
        r = requests.post(
            "https://dpaste.org/api/",
            data={
                "content": teks,
                "syntax": "text",
                "expiry_days": 1,
            },
            timeout=10
        )
        if r.status_code == 200 or r.status_code == 201:
            link = r.text.strip().strip('"')
            if link.startswith("http"):
                return {"link": link, "judul": judul}
        return None
    except Exception as e:
        return None
