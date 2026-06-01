import requests

def shorten_url(url):
    """Perpendek URL menggunakan TinyURL API (gratis, tanpa API key)"""
    try:
        if not url.startswith("http"):
            url = "https://" + url

        r = requests.get(f"https://tinyurl.com/api-create.php?url={url}", timeout=10)
        if r.status_code == 200 and r.text.startswith("http"):
            return {
                "url_asli": url,
                "url_pendek": r.text.strip()
            }
        return None
    except Exception as e:
        return None
