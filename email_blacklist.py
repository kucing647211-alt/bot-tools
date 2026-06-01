import requests

def cek_blacklist(email_atau_domain):
    """Cek apakah email/domain masuk blacklist spam via public API"""
    try:
        # Ambil domain dari email
        if "@" in email_atau_domain:
            domain = email_atau_domain.split("@")[1]
            input_type = "email"
        else:
            domain = email_atau_domain.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
            input_type = "domain"

        # Cek via HaveIBeenPwned untuk email
        pwned = False
        pwned_count = 0
        if input_type == "email":
            try:
                r = requests.get(
                    f"https://haveibeenpwned.com/api/v2/breachedaccount/{email_atau_domain}",
                    headers={"User-Agent": "BotTools-Checker"},
                    timeout=8
                )
                if r.status_code == 200:
                    pwned = True
                    pwned_count = len(r.json())
            except:
                pass

        # Cek domain via disposable email list
        disposable = False
        try:
            r2 = requests.get(
                f"https://disposable.debounce.io/?email=test@{domain}",
                timeout=8
            )
            if r2.status_code == 200:
                disposable = r2.json().get("disposable", "false") == "true"
        except:
            pass

        return {
            "input": email_atau_domain,
            "domain": domain,
            "type": input_type,
            "pwned": pwned,
            "pwned_count": pwned_count,
            "disposable": disposable,
        }
    except Exception as e:
        return None

def format_hasil(data):
    pwned_info = f"⚠️ Ya, bocor di *{data['pwned_count']} breach*!" if data["pwned"] else "✅ Tidak ditemukan di breach database"
    disposable_info = "⚠️ Ya (email sementara/disposable)" if data["disposable"] else "✅ Bukan email disposable"

    status_overall = "🔴 *BERISIKO*" if (data["pwned"] or data["disposable"]) else "🟢 *AMAN*"

    teks = (
        f"🧹 *Cek Email Blacklist*\n\n"
        f"📧 *Input:* `{data['input']}`\n"
        f"🌐 *Domain:* `{data['domain']}`\n\n"
        f"🔓 *Data Breach (HIBP):*\n{pwned_info}\n\n"
        f"🗑️ *Disposable Email:*\n{disposable_info}\n\n"
        f"📊 *Status Keseluruhan:* {status_overall}\n\n"
    )

    if data["pwned"]:
        teks += "💡 _Saran: Ganti password akun yang pakai email ini segera!_"
    else:
        teks += "💡 _Email ini relatif aman digunakan._"

    return teks
