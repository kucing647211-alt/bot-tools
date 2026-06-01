# 🤖 Bot Tools Telegram — 15 Fitur Gratis

Bot Telegram lengkap dengan 15 fitur tools, semua gratis tanpa modal.

## ✨ 15 Fitur Lengkap

| # | Fitur | Deskripsi | Sumber |
|---|-------|-----------|--------|
| 1 | 📧 Email Sementara | Buat email sekali pakai, cek inbox langsung di bot | Mail.tm |
| 2 | 📱 Nomor Virtual | Nomor publik untuk terima SMS | receive-smss.com |
| 3 | 🌐 Translate Teks | Terjemahkan ke 10+ bahasa | deep-translator |
| 4 | 💱 Konversi Mata Uang | Kurs real-time 10 mata uang | exchangerate-api.com |
| 5 | 🖼️ Reverse Image | Cari asal usul gambar via 4 mesin | Google/TinEye/Yandex/Bing |
| 6 | ⬆️ Cek Status Website | Cek website up/down + kecepatan respon | requests |
| 7 | 🔗 URL Shortener | Perpendek link panjang | TinyURL API |
| 8 | 📋 Pastebin Sementara | Simpan teks/kode, dapat link 1 hari | dpaste.org |
| 9 | 📍 IP Tracker | Info detail IP: negara, kota, ISP, koordinat, proxy | ip-api.com |
| 10 | 🎲 Nama Palsu | Generate identitas dummy lengkap | Built-in |
| 11 | 🔍 Cek Username | Cari username di 15+ platform sosmed | requests |
| 12 | 💻 Hash Generator | Convert teks ke MD5/SHA1/SHA256/SHA512 | hashlib |
| 13 | 🌐 Whois Domain | Info registrasi & status domain | rdap.org |
| 14 | 🧹 Cek Email Blacklist | Cek breach & disposable email | HIBP + debounce.io |
| 15 | 🌈 Warna Hex/RGB | Convert HEX↔RGB, tampilkan HSL & CSS | Built-in |

## 🚀 Cara Deploy ke Railway (Gratis)

### Step 1 — Buat Bot Telegram
1. Buka Telegram → cari **@BotFather**
2. Kirim `/newbot` → ikuti instruksi
3. Copy **TOKEN** yang diberikan

### Step 2 — Upload ke GitHub
1. Buat repo baru di [github.com](https://github.com)
2. Upload semua file dari zip ini ke repo

### Step 3 — Deploy ke Railway
1. Buka [railway.app](https://railway.app) → login pakai GitHub
2. Klik **New Project** → **Deploy from GitHub repo**
3. Pilih repo bot kamu
4. Klik tab **Variables** → tambah:
   ```
   BOT_TOKEN = token_dari_botfather
   ```
5. Klik **Deploy** → bot langsung jalan! 🎉

## 🖥️ Jalankan Lokal (Testing)

```bash
pip install -r requirements.txt
export BOT_TOKEN=token_kamu   # Linux/Mac
set BOT_TOKEN=token_kamu      # Windows
python main.py
```

## 📁 Struktur File

```
bot-tools/
├── main.py
├── features/
│   ├── email_temp.py
│   ├── nomor_virtual.py
│   ├── translate.py
│   ├── currency.py
│   ├── reverse_image.py
│   ├── status_website.py
│   ├── url_shortener.py
│   ├── pastebin.py
│   ├── ip_tracker.py
│   ├── nama_palsu.py
│   ├── cek_username.py
│   ├── hash_generator.py
│   ├── whois_domain.py
│   ├── email_blacklist.py
│   └── warna_hex.py
├── requirements.txt
├── Procfile
└── README.md
```

## ⚠️ Catatan
- Semua fitur **100% gratis**, tidak perlu kartu kredit
- Nomor virtual adalah nomor **publik/shared**
- Email sementara expired otomatis setelah beberapa jam
- Pastebin link aktif **1 hari**
- Cek username butuh ~15-30 detik karena cek banyak platform
