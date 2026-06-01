import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
import email_temp, nomor_virtual, translate, currency, reverse_image, status_website, url_shortener, pastebin, ip_tracker, nama_palsu, cek_username, hash_generator, whois_domain, email_blacklist, warna_hex

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "8909043565:AAE0MNKwzzCaMafVh3rElLITx0roMlAbhBg")

# ===================== WARNA TOMBOL =====================
# Bot API 9.4 - style: "primary" (biru), "success" (hijau), "danger" (merah)
PRIMARY = "primary"   # 🔵 Biru
SUCCESS = "success"   # 🟢 Hijau
DANGER  = "danger"    # 🔴 Merah

def btn(text, data, style=None):
    """Helper buat InlineKeyboardButton dengan optional style warna"""
    return InlineKeyboardButton(text, callback_data=data, style=style)

# ===================== KEYBOARD UTAMA =====================
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [btn("📧 Email Sementara", "menu_email", SUCCESS),
         btn("📱 Nomor Virtual", "menu_nomor", SUCCESS)],
        [btn("🌐 Translate Teks", "menu_translate", PRIMARY),
         btn("💱 Konversi Mata Uang", "menu_currency", PRIMARY)],
        [btn("🖼️ Reverse Image", "menu_image", PRIMARY),
         btn("⬆️ Cek Status Web", "menu_status", PRIMARY)],
        [btn("🔗 URL Shortener", "menu_short", PRIMARY),
         btn("📋 Pastebin", "menu_paste", PRIMARY)],
        [btn("📍 IP Tracker", "menu_ip", PRIMARY),
         btn("🎲 Nama Palsu", "menu_nama", PRIMARY)],
        [btn("🔍 Cek Username", "menu_username", PRIMARY),
         btn("💻 Hash Generator", "menu_hash", PRIMARY)],
        [btn("🌐 Whois Domain", "menu_whois", PRIMARY),
         btn("🧹 Email Blacklist", "menu_blacklist", DANGER)],
        [btn("🌈 Warna Hex/RGB", "menu_warna", PRIMARY)],
    ])

def back_btn():
    return InlineKeyboardMarkup([[btn("🔙 Menu Utama", "menu_back", DANGER)]])

# ===================== TEKS MENU UTAMA (HTML + blockquote) =====================
MAIN_MENU_TEXT = (
    "👋 <b>Selamat datang di Free Tools Bot!</b>\n\n"
    "<blockquote>🔧 Bot ini menyediakan 15 tools gratis "
    "tanpa perlu modal, semua bisa diakses langsung dari Telegram.</blockquote>\n\n"
    "📋 <b>Daftar Fitur:</b>\n"
    "📧 Email Sementara • 📱 Nomor Virtual\n"
    "🌐 Translate • 💱 Mata Uang\n"
    "🖼️ Reverse Image • ⬆️ Status Web\n"
    "🔗 URL Shortener • 📋 Pastebin\n"
    "📍 IP Tracker • 🎲 Nama Palsu\n"
    "🔍 Cek Username • 💻 Hash Generator\n"
    "🌐 Whois Domain • 🧹 Email Blacklist\n"
    "🌈 Warna Hex/RGB\n\n"
    "⬇️ <b>Pilih menu di bawah:</b>"
)

# ===================== /start =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MAIN_MENU_TEXT, parse_mode=ParseMode.HTML, reply_markup=main_menu_keyboard())

# ===================== MENU CALLBACK =====================
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ---- EMAIL ----
    if data == "menu_email":
        await query.edit_message_text(
            "📧 <b>Email Sementara</b>\n\n"
            "<blockquote>Buat email sekali pakai yang bisa menerima email masuk. "
            "Cocok untuk daftar akun tanpa pakai email asli kamu.</blockquote>\n\n"
            "⚠️ Email akan expired otomatis setelah beberapa jam.\n\n"
            "Pilih aksi:",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [btn("✉️ Buat Email Baru", "email_buat", SUCCESS)],
                [btn("📬 Cek Inbox", "email_inbox", PRIMARY)],
                [btn("🔙 Menu Utama", "menu_back", DANGER)],
            ])
        )

    elif data == "email_buat":
        await query.edit_message_text("⏳ Membuat email baru, tunggu sebentar...")
        hasil = email_temp.buat_email()
        if hasil:
            context.user_data["email_token"] = hasil["token"]
            context.user_data["email_address"] = hasil["email"]
            await query.edit_message_text(
                f"✅ <b>Email Sementara Berhasil Dibuat!</b>\n\n"
                f"📧 Email: <code>{hasil['email']}</code>\n"
                f"🔑 Password: <code>{hasil['password']}</code>\n\n"
                f"<blockquote>💡 Gunakan email ini untuk daftar atau verifikasi akun. "
                f"Simpan info ini karena tidak bisa ditampilkan ulang!</blockquote>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([
                    [btn("📬 Cek Inbox", "email_inbox", SUCCESS)],
                    [btn("✉️ Buat Email Baru Lagi", "email_buat", PRIMARY)],
                    [btn("🔙 Menu Utama", "menu_back", DANGER)],
                ])
            )
        else:
            await query.edit_message_text("❌ Gagal membuat email. Coba lagi.",
                reply_markup=InlineKeyboardMarkup([
                    [btn("🔄 Coba Lagi", "email_buat", SUCCESS),
                     btn("🔙 Kembali", "menu_email", DANGER)]
                ]))

    elif data == "email_inbox":
        token = context.user_data.get("email_token")
        email = context.user_data.get("email_address")
        if not token:
            await query.edit_message_text(
                "⚠️ Kamu belum punya email aktif. Buat dulu ya!",
                reply_markup=InlineKeyboardMarkup([
                    [btn("✉️ Buat Email", "email_buat", SUCCESS)],
                    [btn("🔙 Kembali", "menu_email", DANGER)]
                ]))
            return
        await query.edit_message_text("⏳ Mengecek inbox...")
        messages = email_temp.cek_inbox(token)
        if not messages:
            await query.edit_message_text(
                f"📭 <b>Inbox Kosong</b>\n\nEmail: <code>{email}</code>\n\n"
                f"<blockquote>Tunggu email masuk lalu tekan Refresh.</blockquote>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([
                    [btn("🔄 Refresh", "email_inbox", SUCCESS)],
                    [btn("🔙 Kembali", "menu_email", DANGER)],
                ])
            )
        else:
            teks = f"📬 <b>Inbox:</b> <code>{email}</code>\n\n"
            keyboard = []
            for i, msg in enumerate(messages[:5]):
                subjek = msg.get("subject", "Tanpa Subjek")[:40]
                pengirim = msg.get("from", {}).get("address", "?")
                teks += f"<b>{i+1}.</b> {subjek}\n    📤 {pengirim}\n\n"
                keyboard.append([btn(f"📖 Baca #{i+1}: {subjek[:25]}", f"email_baca_{msg['id']}", PRIMARY)])
            keyboard.append([btn("🔄 Refresh", "email_inbox", SUCCESS)])
            keyboard.append([btn("🔙 Kembali", "menu_email", DANGER)])
            await query.edit_message_text(teks, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("email_baca_"):
        msg_id = data.replace("email_baca_", "")
        token = context.user_data.get("email_token")
        msg = email_temp.baca_email(token, msg_id)
        if msg:
            subjek = msg.get("subject", "Tanpa Subjek")
            pengirim = msg.get("from", {}).get("address", "?")
            isi = msg.get("text", msg.get("html", "Tidak ada isi"))[:1500]
            await query.edit_message_text(
                f"📨 <b>{subjek}</b>\n📤 Dari: <code>{pengirim}</code>\n\n"
                f"<blockquote>{isi}</blockquote>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[btn("🔙 Inbox", "email_inbox", DANGER)]]))

    # ---- NOMOR VIRTUAL ----
    elif data == "menu_nomor":
        await query.edit_message_text("⏳ Mengambil daftar nomor publik...")
        nomor_list = nomor_virtual.ambil_daftar_nomor()
        if not nomor_list:
            await query.edit_message_text("❌ Gagal mengambil daftar nomor.", reply_markup=back_btn())
            return
        keyboard = []
        for nomor in nomor_list[:6]:
            keyboard.append([btn(f"📱 {nomor}", f"nomor_cek_{nomor}", SUCCESS)])
        keyboard.append([btn("🔄 Refresh Daftar", "menu_nomor", PRIMARY)])
        keyboard.append([btn("🔙 Menu Utama", "menu_back", DANGER)])
        await query.edit_message_text(
            "📱 <b>Nomor Virtual Publik</b>\n\n"
            "<blockquote>⚠️ Nomor ini bersifat publik dan bisa dilihat semua orang. "
            "Cocok untuk verifikasi platform kecil atau testing.</blockquote>\n\n"
            "Pilih nomor untuk lihat SMS masuk:",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("nomor_cek_"):
        nomor = data.replace("nomor_cek_", "")
        await query.edit_message_text(f"⏳ Mengecek SMS untuk <code>{nomor}</code>...", parse_mode=ParseMode.HTML)
        sms_list = nomor_virtual.cek_sms_nomor(nomor)
        keyboard = InlineKeyboardMarkup([
            [btn("🔄 Refresh", f"nomor_cek_{nomor}", SUCCESS)],
            [btn("🔙 Pilih Nomor Lain", "menu_nomor", DANGER)]
        ])
        if not sms_list:
            await query.edit_message_text(
                f"📭 <b>Belum ada SMS</b>\n\nNomor: <code>{nomor}</code>\n\n"
                f"<blockquote>Tunggu SMS masuk lalu tekan Refresh.</blockquote>",
                parse_mode=ParseMode.HTML, reply_markup=keyboard)
        else:
            teks = f"📱 <b>SMS untuk</b> <code>{nomor}</code>\n\n"
            for sms in sms_list:
                teks += f"📤 <b>Dari:</b> {sms['pengirim']}\n💬 <b>Pesan:</b> {sms['pesan']}\n🕐 {sms['waktu']}\n──────────\n"
            await query.edit_message_text(teks, parse_mode=ParseMode.HTML, reply_markup=keyboard)

    # ---- TRANSLATE ----
    elif data == "menu_translate":
        bahasa_dict = translate.daftar_bahasa()
        keyboard = []
        row = []
        for kode, nama in bahasa_dict.items():
            row.append(btn(nama, f"translate_{kode}", PRIMARY))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        keyboard.append([btn("🔙 Menu Utama", "menu_back", DANGER)])
        await query.edit_message_text(
            "🌐 <b>Translate Teks</b>\n\n"
            "<blockquote>Pilih bahasa tujuan, lalu kirim teks yang ingin diterjemahkan.</blockquote>",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("translate_"):
        kode_bahasa = data.replace("translate_", "")
        context.user_data["translate_target"] = kode_bahasa
        context.user_data["waiting_for"] = "translate"
        nama_bahasa = translate.daftar_bahasa().get(kode_bahasa, kode_bahasa)
        await query.edit_message_text(
            f"🌐 <b>Translate ke {nama_bahasa}</b>\n\n"
            f"<blockquote>Kirim teks yang ingin diterjemahkan. Bisa kirim berkali-kali tanpa perlu pilih bahasa lagi.</blockquote>",
            parse_mode=ParseMode.HTML)

    # ---- CURRENCY ----
    elif data == "menu_currency":
        keyboard = []
        row = []
        for mu in currency.MATA_UANG_POPULER:
            row.append(btn(mu, f"currency_dari_{mu}", PRIMARY))
            if len(row) == 3:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        keyboard.append([btn("🔙 Menu Utama", "menu_back", DANGER)])
        await query.edit_message_text(
            "💱 <b>Konversi Mata Uang</b>\n\n"
            "<blockquote>Pilih mata uang asal terlebih dahulu.</blockquote>",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("currency_dari_"):
        dari = data.replace("currency_dari_", "")
        context.user_data["currency_dari"] = dari
        keyboard = []
        row = []
        for mu in [m for m in currency.MATA_UANG_POPULER if m != dari]:
            row.append(btn(mu, f"currency_ke_{mu}", SUCCESS))
            if len(row) == 3:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        keyboard.append([btn("🔙 Kembali", "menu_currency", DANGER)])
        await query.edit_message_text(
            f"💱 Dari <b>{dari}</b> → Pilih mata uang <b>tujuan</b>:",
            parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("currency_ke_"):
        ke = data.replace("currency_ke_", "")
        context.user_data["currency_ke"] = ke
        context.user_data["waiting_for"] = "currency"
        dari = context.user_data.get("currency_dari")
        await query.edit_message_text(
            f"💱 Konversi <b>{dari}</b> → <b>{ke}</b>\n\n"
            f"<blockquote>Ketik jumlah yang ingin dikonversi.\nContoh: <code>100000</code></blockquote>",
            parse_mode=ParseMode.HTML)

    # ---- REVERSE IMAGE ----
    elif data == "menu_image":
        context.user_data["waiting_for"] = "image"
        await query.edit_message_text(
            "🖼️ <b>Reverse Image Search</b>\n\n"
            "<blockquote>Kirim URL gambar untuk dicari asal usulnya. "
            "Bot akan kasih link ke Google Images, TinEye, Yandex, dan Bing sekaligus.</blockquote>\n\n"
            "Contoh: <code>https://example.com/foto.jpg</code>",
            parse_mode=ParseMode.HTML)

    # ---- STATUS WEBSITE ----
    elif data == "menu_status":
        context.user_data["waiting_for"] = "status"
        await query.edit_message_text(
            "⬆️ <b>Cek Status Website</b>\n\n"
            "<blockquote>Kirim URL website untuk dicek. Bot akan tampilkan status UP/DOWN, "
            "kecepatan respon dalam milidetik, dan HTTP status code.</blockquote>\n\n"
            "Contoh: <code>google.com</code> atau <code>https://tokopedia.com</code>",
            parse_mode=ParseMode.HTML)

    # ---- URL SHORTENER ----
    elif data == "menu_short":
        context.user_data["waiting_for"] = "short"
        await query.edit_message_text(
            "🔗 <b>URL Shortener</b>\n\n"
            "<blockquote>Kirim URL panjang yang ingin diperpendek. "
            "Menggunakan TinyURL, gratis tanpa perlu daftar akun.</blockquote>\n\n"
            "Contoh:\n<code>https://www.tokopedia.com/product/very-long-url-here</code>",
            parse_mode=ParseMode.HTML)

    # ---- PASTEBIN ----
    elif data == "menu_paste":
        context.user_data["waiting_for"] = "paste"
        await query.edit_message_text(
            "📋 <b>Pastebin Sementara</b>\n\n"
            "<blockquote>Kirim teks atau kode yang ingin disimpan. "
            "Bot akan kasih link yang bisa dibuka di browser dan dibagikan ke siapapun.</blockquote>\n\n"
            "⚠️ Link aktif selama <b>1 hari</b>.",
            parse_mode=ParseMode.HTML)

    # ---- IP TRACKER ----
    elif data == "menu_ip":
        context.user_data["waiting_for"] = "ip"
        await query.edit_message_text(
            "📍 <b>IP Tracker</b>\n\n"
            "<blockquote>Kirim IP address untuk dicek. Bot akan tampilkan negara, kota, "
            "ISP, koordinat lengkap dengan link Google Maps, serta status Proxy/VPN.</blockquote>\n\n"
            "Contoh: <code>8.8.8.8</code> atau <code>1.1.1.1</code>\n"
            "Ketik <code>saya</code> untuk cek IP kamu sendiri.",
            parse_mode=ParseMode.HTML)

    # ---- NAMA PALSU ----
    elif data == "menu_nama":
        hasil = nama_palsu.generate_identitas()
        teks = nama_palsu.format_identitas(hasil)
        # Convert markdown to HTML
        teks_html = teks.replace("*", "<b>", 1)
        await query.edit_message_text(
            f"🎲 <b>Identitas Dummy</b>\n\n"
            f"<blockquote>Data berikut sepenuhnya fiktif, hanya untuk keperluan testing form atau UI.</blockquote>\n\n"
            f"👤 <b>Nama:</b> {hasil['nama']}\n"
            f"🎂 <b>Tgl Lahir:</b> {hasil['tgl_lahir']}\n"
            f"💼 <b>Pekerjaan:</b> {hasil['pekerjaan']}\n"
            f"📧 <b>Email:</b> <code>{hasil['email']}</code>\n"
            f"📱 <b>No. HP:</b> <code>{hasil['nomor_hp']}</code>\n"
            f"🏠 <b>Alamat:</b> {hasil['alamat']}\n"
            f"👾 <b>Username:</b> <code>{hasil['username']}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [btn("🔄 Generate Ulang", "menu_nama", SUCCESS)],
                [btn("🔙 Menu Utama", "menu_back", DANGER)],
            ]))

    # ---- CEK USERNAME ----
    elif data == "menu_username":
        context.user_data["waiting_for"] = "username"
        await query.edit_message_text(
            "🔍 <b>Cek Username</b>\n\n"
            "<blockquote>Kirim username yang ingin dicek. Bot akan cek ketersediaannya "
            "di 15+ platform sekaligus: Instagram, TikTok, Twitter/X, GitHub, Reddit, "
            "Telegram, YouTube, Twitch, Pinterest, dan lainnya.</blockquote>\n\n"
            "⏳ Proses sekitar 15–30 detik.\n\nContoh: <code>johndoe123</code>",
            parse_mode=ParseMode.HTML)

    # ---- HASH GENERATOR ----
    elif data == "menu_hash":
        context.user_data["waiting_for"] = "hash"
        await query.edit_message_text(
            "💻 <b>Hash Generator</b>\n\n"
            "<blockquote>Kirim teks apapun dan bot akan generate hash MD5, SHA1, SHA256, "
            "dan SHA512 sekaligus. Berguna untuk verifikasi integritas data.</blockquote>\n\n"
            "⚠️ Hash tidak bisa di-decrypt.\n\nContoh: <code>password123</code>",
            parse_mode=ParseMode.HTML)

    # ---- WHOIS DOMAIN ----
    elif data == "menu_whois":
        context.user_data["waiting_for"] = "whois"
        await query.edit_message_text(
            "🌐 <b>Whois Domain</b>\n\n"
            "<blockquote>Kirim nama domain untuk dicek. Bot akan tampilkan status domain, "
            "tanggal dibuat, tanggal expired, dan nameserver.</blockquote>\n\n"
            "Contoh: <code>google.com</code> atau <code>tokopedia.com</code>",
            parse_mode=ParseMode.HTML)

    # ---- EMAIL BLACKLIST ----
    elif data == "menu_blacklist":
        context.user_data["waiting_for"] = "blacklist"
        await query.edit_message_text(
            "🧹 <b>Cek Email Blacklist</b>\n\n"
            "<blockquote>Kirim email atau domain untuk dicek. Bot akan cek apakah pernah "
            "bocor di data breach dan apakah termasuk email disposable/spam.</blockquote>\n\n"
            "Contoh:\n<code>contoh@gmail.com</code>\n<code>tokopedia.com</code>",
            parse_mode=ParseMode.HTML)

    # ---- WARNA HEX ----
    elif data == "menu_warna":
        context.user_data["waiting_for"] = "warna"
        await query.edit_message_text(
            "🌈 <b>Konverter Warna Hex/RGB</b>\n\n"
            "<blockquote>Kirim kode warna dan bot akan konversi ke semua format: "
            "HEX, RGB, HSL, lengkap dengan nama warna dan CSS siap pakai.</blockquote>\n\n"
            "Format yang diterima:\n"
            "• <code>#FF5733</code>\n"
            "• <code>FF5733</code>\n"
            "• <code>255, 87, 51</code>\n"
            "• <code>rgb(255, 87, 51)</code>",
            parse_mode=ParseMode.HTML)

    # ---- BACK ----
    elif data == "menu_back":
        await query.edit_message_text(MAIN_MENU_TEXT, parse_mode=ParseMode.HTML, reply_markup=main_menu_keyboard())

# ===================== HANDLER PESAN TEKS =====================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    waiting = context.user_data.get("waiting_for")
    teks = update.message.text.strip()

    if waiting == "translate":
        target = context.user_data.get("translate_target", "en")
        nama_bahasa = translate.daftar_bahasa().get(target, target)
        await update.message.reply_text("⏳ Menerjemahkan...")
        hasil = translate.translate_teks(teks, bahasa_tujuan=target)
        if hasil:
            await update.message.reply_text(
                f"🌐 <b>Hasil ke {nama_bahasa}:</b>\n\n<blockquote>{hasil}</blockquote>\n\nKirim teks lain atau /start.",
                parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text("❌ Gagal menerjemahkan. Coba lagi atau /start.")

    elif waiting == "currency":
        try:
            jumlah = float(teks.replace(",", "."))
            dari = context.user_data.get("currency_dari")
            ke = context.user_data.get("currency_ke")
            await update.message.reply_text("⏳ Mengambil kurs terbaru...")
            hasil = currency.konversi_mata_uang(jumlah, dari, ke)
            if hasil:
                await update.message.reply_text(
                    f"💱 <b>Hasil Konversi:</b>\n\n"
                    f"<blockquote><code>{jumlah:,.2f} {dari}</code> = <code>{hasil['hasil']:,.2f} {ke}</code>\n\n"
                    f"📊 Kurs: 1 {dari} = {hasil['rate']} {ke}</blockquote>\n\nKetik jumlah lain atau /start.",
                    parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text("❌ Gagal ambil kurs. Coba lagi atau /start.")
        except ValueError:
            await update.message.reply_text("⚠️ Masukkan angka yang valid. Contoh: <code>100000</code>", parse_mode=ParseMode.HTML)

    elif waiting == "image":
        if teks.startswith("http"):
            links = reverse_image.reverse_image_search(teks)
            hasil = "🖼️ <b>Reverse Image Search:</b>\n\n"
            for nama, url in links.items():
                hasil += f"🔍 <a href='{url}'>{nama}</a>\n"
            await update.message.reply_text(hasil + "\nKlik link di atas untuk mencari gambar.",
                parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        else:
            await update.message.reply_text("⚠️ URL harus dimulai dengan <code>http</code> atau <code>https</code>", parse_mode=ParseMode.HTML)

    elif waiting == "status":
        await update.message.reply_text(f"⏳ Mengecek <code>{teks}</code>...", parse_mode=ParseMode.HTML)
        hasil = status_website.cek_status_website(teks)
        if hasil["status"] == "UP":
            await update.message.reply_text(
                f"✅ <b>Website UP!</b>\n\n"
                f"<blockquote>🌐 {hasil['url']}\n📊 Status Code: <code>{hasil['kode']}</code>\n⚡ Respon: <code>{hasil['waktu_ms']} ms</code></blockquote>\n\nKirim URL lain atau /start.",
                parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text(
                f"❌ <b>Website DOWN!</b>\n\n"
                f"<blockquote>🌐 {hasil['url']}\n📊 Status Code: <code>{hasil['kode']}</code>\n⚠️ {hasil.get('error', '-')}</blockquote>\n\nKirim URL lain atau /start.",
                parse_mode=ParseMode.HTML)

    elif waiting == "short":
        if "." in teks:
            await update.message.reply_text("⏳ Memperpendek URL...")
            hasil = url_shortener.shorten_url(teks)
            if hasil:
                await update.message.reply_text(
                    f"🔗 <b>Berhasil Diperpendek!</b>\n\n"
                    f"<blockquote>📎 Asli:\n<code>{hasil['url_asli']}</code>\n\n✂️ Pendek:\n<code>{hasil['url_pendek']}</code></blockquote>\n\nKirim URL lain atau /start.",
                    parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text("❌ Gagal memperpendek. Pastikan URL valid.")
        else:
            await update.message.reply_text("⚠️ Kirim URL yang valid. Contoh: <code>https://google.com</code>", parse_mode=ParseMode.HTML)

    elif waiting == "paste":
        if len(teks) < 5:
            await update.message.reply_text("⚠️ Teks terlalu pendek, minimal 5 karakter.")
            return
        await update.message.reply_text("⏳ Menyimpan ke pastebin...")
        hasil = pastebin.simpan_pastebin(teks)
        if hasil:
            await update.message.reply_text(
                f"📋 <b>Teks Berhasil Disimpan!</b>\n\n"
                f"<blockquote>🔗 Link: {hasil['link']}\n⚠️ Aktif selama 1 hari.</blockquote>\n\nKirim teks lain atau /start.",
                parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        else:
            await update.message.reply_text("❌ Gagal menyimpan. Coba lagi atau /start.")

    elif waiting == "ip":
        await update.message.reply_text("⏳ Melacak IP...")
        hasil = ip_tracker.cek_ip() if teks.lower() == "saya" else ip_tracker.cek_ip(teks)
        if hasil:
            maps_link = f"https://maps.google.com/?q={hasil['lat']},{hasil['lon']}"
            proxy_status = "⚠️ Ya" if hasil["proxy"] else "✅ Tidak"
            mobile_status = "📱 Ya" if hasil["mobile"] else "💻 Tidak"
            await update.message.reply_text(
                f"📍 <b>Hasil IP Tracker</b>\n\n"
                f"<blockquote>"
                f"🌐 <b>IP:</b> <code>{hasil['ip']}</code>\n"
                f"🏳️ <b>Negara:</b> {hasil['negara']} ({hasil['kode_negara']})\n"
                f"🏙️ <b>Kota:</b> {hasil['kota']}, {hasil['wilayah']}\n"
                f"📡 <b>ISP:</b> {hasil['isp']}\n"
                f"🕐 <b>Timezone:</b> {hasil['timezone']}\n"
                f"📍 <b>Koordinat:</b> <code>{hasil['lat']}, {hasil['lon']}</code>\n"
                f"🔒 <b>Proxy/VPN:</b> {proxy_status}\n"
                f"📱 <b>Mobile:</b> {mobile_status}"
                f"</blockquote>\n\n"
                f"🗺️ <a href='{maps_link}'>Lihat di Google Maps</a>\n\nKirim IP lain, ketik <code>saya</code>, atau /start.",
                parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        else:
            await update.message.reply_text("❌ IP tidak valid. Coba lagi atau /start.")

    elif waiting == "username":
        if len(teks) < 2:
            await update.message.reply_text("⚠️ Username minimal 2 karakter.")
            return
        await update.message.reply_text(
            f"⏳ Mencari username <code>{teks}</code> di 15+ platform...\nProses ~15–30 detik, harap tunggu.",
            parse_mode=ParseMode.HTML)
        hasil = cek_username.cek_username(teks)
        ada = [(p, d["url"]) for p, d in hasil.items() if d["status"] == "ADA"]
        kosong = [p for p, d in hasil.items() if d["status"] == "KOSONG"]
        teks_hasil = f"🔍 <b>Hasil Cek Username:</b> <code>{teks}</code>\n\n"
        if ada:
            teks_hasil += f"✅ <b>Ditemukan di {len(ada)} platform:</b>\n"
            for platform, url in ada:
                teks_hasil += f"• <a href='{url}'>{platform}</a>\n"
            teks_hasil += "\n"
        if kosong:
            teks_hasil += f"<blockquote>⭕ Tersedia di {len(kosong)} platform:\n"
            teks_hasil += ", ".join(kosong) + "</blockquote>"
        await update.message.reply_text(teks_hasil, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        await update.message.reply_text("Kirim username lain atau /start untuk menu.")

    elif waiting == "hash":
        hasil = hash_generator.generate_hash(teks)
        await update.message.reply_text(
            f"💻 <b>Hash Generator</b>\n\n"
            f"📝 <b>Input:</b> <code>{teks[:50]}{'...' if len(teks) > 50 else ''}</code>\n\n"
            f"<blockquote>"
            f"🔐 <b>MD5:</b>\n<code>{hasil['MD5']}</code>\n\n"
            f"🔐 <b>SHA1:</b>\n<code>{hasil['SHA1']}</code>\n\n"
            f"🔐 <b>SHA256:</b>\n<code>{hasil['SHA256']}</code>\n\n"
            f"🔐 <b>SHA512:</b>\n<code>{hasil['SHA512'][:64]}...</code>"
            f"</blockquote>",
            parse_mode=ParseMode.HTML)
        await update.message.reply_text("Kirim teks lain untuk di-hash atau /start untuk menu.")

    elif waiting == "whois":
        await update.message.reply_text(f"⏳ Mengecek whois <code>{teks}</code>...", parse_mode=ParseMode.HTML)
        hasil = whois_domain.cek_whois_rdap(teks)
        if hasil:
            ns = "\n".join([f"• <code>{n}</code>" for n in hasil.get("nameservers", [])]) or "• ?"
            await update.message.reply_text(
                f"🌐 <b>Whois Domain</b>\n\n"
                f"<blockquote>"
                f"🔎 <b>Domain:</b> <code>{hasil['domain']}</code>\n"
                f"📋 <b>Status:</b> {hasil['status']}\n"
                f"📅 <b>Dibuat:</b> {hasil['dibuat']}\n"
                f"⏳ <b>Expired:</b> {hasil['expired']}\n"
                f"🔄 <b>Update:</b> {hasil['updated']}\n"
                f"🖥️ <b>Nameserver:</b>\n{ns}"
                f"</blockquote>",
                parse_mode=ParseMode.HTML)
            await update.message.reply_text("Kirim domain lain atau /start untuk menu.")
        else:
            await update.message.reply_text("❌ Domain tidak ditemukan. Contoh: <code>google.com</code>", parse_mode=ParseMode.HTML)

    elif waiting == "blacklist":
        if "@" not in teks and "." not in teks:
            await update.message.reply_text("⚠️ Masukkan email atau domain yang valid.", parse_mode=ParseMode.HTML)
            return
        await update.message.reply_text(f"⏳ Mengecek <code>{teks}</code>...", parse_mode=ParseMode.HTML)
        hasil = email_blacklist.cek_blacklist(teks)
        if hasil:
            pwned_info = f"⚠️ Ya, bocor di <b>{hasil['pwned_count']} breach!</b>" if hasil["pwned"] else "✅ Tidak ditemukan di breach database"
            disposable_info = "⚠️ Ya (email disposable/spam)" if hasil["disposable"] else "✅ Bukan email disposable"
            status = "🔴 <b>BERISIKO</b>" if (hasil["pwned"] or hasil["disposable"]) else "🟢 <b>AMAN</b>"
            await update.message.reply_text(
                f"🧹 <b>Cek Email Blacklist</b>\n\n"
                f"📧 <b>Input:</b> <code>{hasil['input']}</code>\n\n"
                f"<blockquote>"
                f"🔓 <b>Data Breach:</b>\n{pwned_info}\n\n"
                f"🗑️ <b>Disposable:</b>\n{disposable_info}\n\n"
                f"📊 <b>Status:</b> {status}"
                f"</blockquote>",
                parse_mode=ParseMode.HTML)
            await update.message.reply_text("Kirim email/domain lain atau /start untuk menu.")
        else:
            await update.message.reply_text("❌ Gagal mengecek. Coba lagi atau /start.")

    elif waiting == "warna":
        tipe, nilai = warna_hex.parse_input(teks)
        if tipe == "hex":
            hasil = warna_hex.hex_ke_rgb(nilai)
        elif tipe == "rgb":
            hasil = warna_hex.rgb_ke_hex(*nilai)
        else:
            await update.message.reply_text(
                "⚠️ Format tidak dikenali.\n\nContoh:\n• <code>#FF5733</code>\n• <code>255, 87, 51</code>",
                parse_mode=ParseMode.HTML)
            return
        if hasil:
            r, g, b = hasil["r"], hasil["g"], hasil["b"]
            nama = warna_hex.nama_warna_approx(r, g, b)
            h, s, l = warna_hex.hsl_dari_rgb(r, g, b)
            await update.message.reply_text(
                f"🌈 <b>Konverter Warna</b>\n\n"
                f"🎨 <b>Warna:</b> {nama}\n\n"
                f"<blockquote>"
                f"🔢 <b>HEX:</b> <code>{hasil['hex']}</code>\n"
                f"🔴 <b>RGB:</b> <code>rgb({r}, {g}, {b})</code>\n"
                f"🌀 <b>HSL:</b> <code>hsl({h}°, {s}%, {l}%)</code>\n\n"
                f"📋 <b>CSS:</b>\n<code>color: {hasil['hex']};</code>\n"
                f"<code>background: rgb({r}, {g}, {b});</code>"
                f"</blockquote>",
                parse_mode=ParseMode.HTML)
            await update.message.reply_text("Kirim warna lain atau /start untuk menu.")
        else:
            await update.message.reply_text("❌ Nilai warna tidak valid. RGB harus antara 0–255.")

    else:
        await update.message.reply_text("Ketik /start untuk membuka menu utama.")

# ===================== MAIN =====================
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot 15 Fitur (Colored Buttons) berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
