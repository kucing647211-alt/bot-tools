import requests

def cek_status_website(url):
    """Cek apakah website up atau down"""
    try:
        # Pastikan ada http/https
        if not url.startswith("http"):
            url = "https://" + url

        r = requests.get(url, timeout=10, allow_redirects=True)
        status_code = r.status_code
        waktu_respon = round(r.elapsed.total_seconds() * 1000)  # ms

        if status_code < 400:
            return {
                "status": "UP",
                "kode": status_code,
                "waktu_ms": waktu_respon,
                "url": url
            }
        else:
            return {
                "status": "DOWN",
                "kode": status_code,
                "waktu_ms": waktu_respon,
                "url": url
            }
    except requests.exceptions.ConnectionError:
        return {"status": "DOWN", "kode": 0, "waktu_ms": 0, "url": url, "error": "Tidak bisa terhubung"}
    except requests.exceptions.Timeout:
        return {"status": "DOWN", "kode": 0, "waktu_ms": 0, "url": url, "error": "Timeout / terlalu lama"}
    except Exception as e:
        return {"status": "ERROR", "kode": 0, "waktu_ms": 0, "url": url, "error": str(e)}
