import requests

def konversi_mata_uang(jumlah, dari, ke):
    """Konversi mata uang menggunakan exchangerate-api gratis"""
    try:
        dari = dari.upper()
        ke = ke.upper()
        url = f"https://api.exchangerate-api.com/v4/latest/{dari}"
        r = requests.get(url, timeout=10)
        data = r.json()
        
        if "rates" not in data:
            return None
        
        rate = data["rates"].get(ke)
        if not rate:
            return None
        
        hasil = jumlah * rate
        return {
            "dari": dari,
            "ke": ke,
            "jumlah": jumlah,
            "hasil": round(hasil, 2),
            "rate": rate
        }
    except Exception as e:
        return None

MATA_UANG_POPULER = ["IDR", "USD", "EUR", "SGD", "MYR", "JPY", "GBP", "AUD", "CNY", "KRW"]
