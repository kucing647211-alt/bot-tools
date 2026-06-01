import requests
import json

BASE_URL = "https://api.mail.tm"

def buat_email():
    """Buat email sementara baru"""
    try:
        # Ambil domain yang tersedia
        domains = requests.get(f"{BASE_URL}/domains").json()
        domain = domains["hydra:member"][0]["domain"]
        
        # Generate email random
        import random, string
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email = f"{username}@{domain}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        # Daftar akun
        r = requests.post(f"{BASE_URL}/accounts", json={"address": email, "password": password})
        if r.status_code == 201:
            # Login ambil token
            token_r = requests.post(f"{BASE_URL}/token", json={"address": email, "password": password})
            token = token_r.json().get("token")
            return {"email": email, "password": password, "token": token}
        else:
            return None
    except Exception as e:
        return None

def cek_inbox(token):
    """Cek inbox email"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(f"{BASE_URL}/messages", headers=headers)
        messages = r.json().get("hydra:member", [])
        return messages
    except:
        return []

def baca_email(token, msg_id):
    """Baca isi email tertentu"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(f"{BASE_URL}/messages/{msg_id}", headers=headers)
        return r.json()
    except:
        return None
