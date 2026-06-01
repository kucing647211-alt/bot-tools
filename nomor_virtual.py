import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def ambil_daftar_nomor():
    """Ambil daftar nomor publik dari receive-smss.com"""
    try:
        r = requests.get("https://receive-smss.com", headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        nomor_list = []
        for item in soup.select(".number-boxes-itemm-number"):
            nomor = item.get_text(strip=True)
            if nomor:
                nomor_list.append(nomor)
        return nomor_list[:10]
    except Exception as e:
        return []

def cek_sms_nomor(nomor):
    """Cek SMS masuk untuk nomor tertentu"""
    try:
        # Bersihkan format nomor
        nomor_bersih = nomor.replace("+", "").replace(" ", "").replace("-", "")
        url = f"https://receive-smss.com/sms/{nomor_bersih}/"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        
        sms_list = []
        rows = soup.select("table tbody tr")
        for row in rows[:5]:  # Ambil 5 SMS terbaru
            cols = row.select("td")
            if len(cols) >= 3:
                pengirim = cols[0].get_text(strip=True)
                pesan = cols[1].get_text(strip=True)
                waktu = cols[2].get_text(strip=True)
                sms_list.append({
                    "pengirim": pengirim,
                    "pesan": pesan,
                    "waktu": waktu
                })
        return sms_list
    except Exception as e:
        return []
