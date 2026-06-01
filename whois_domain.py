import requests

def cek_whois(domain):
    """Cek info whois domain menggunakan whois.freeaiapi.xyz (gratis)"""
    try:
        # Bersihkan domain
        domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]

        r = requests.get(f"https://api.whoisfreaks.com/v1.0/whois?apiKey=free&whois=live&domainName={domain}", timeout=10)
        data = r.json()

        if not data or data.get("status") == "error":
            # Fallback ke rdap
            r2 = requests.get(f"https://rdap.org/domain/{domain}", timeout=10)
            if r2.status_code == 200:
                d = r2.json()
                return {
                    "domain": domain,
                    "status": ", ".join(d.get("status", ["?"])),
                    "registrar": d.get("entities", [{}])[0].get("vcardArray", [[], []])[1][1][3] if d.get("entities") else "?",
                    "dibuat": d.get("events", [{}])[0].get("eventDate", "?")[:10] if d.get("events") else "?",
                    "expired": next((e.get("eventDate", "?")[:10] for e in d.get("events", []) if e.get("eventAction") == "expiration"), "?"),
                    "updated": next((e.get("eventDate", "?")[:10] for e in d.get("events", []) if e.get("eventAction") == "last changed"), "?"),
                    "nameservers": [n.get("ldhName", "") for n in d.get("nameservers", [])][:4],
                }
        return None
    except Exception as e:
        return None

def cek_whois_rdap(domain):
    """Cek whois via RDAP (gratis, tanpa API key)"""
    try:
        domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0].strip()
        r = requests.get(f"https://rdap.org/domain/{domain}", timeout=10)
        if r.status_code != 200:
            return None
        d = r.json()

        nameservers = [n.get("ldhName", "").lower() for n in d.get("nameservers", [])][:4]
        status = d.get("status", ["?"])
        dibuat = next((e.get("eventDate", "?")[:10] for e in d.get("events", []) if e.get("eventAction") == "registration"), "?")
        expired = next((e.get("eventDate", "?")[:10] for e in d.get("events", []) if e.get("eventAction") == "expiration"), "?")
        updated = next((e.get("eventDate", "?")[:10] for e in d.get("events", []) if e.get("eventAction") == "last changed"), "?")

        return {
            "domain": domain,
            "status": ", ".join(status),
            "dibuat": dibuat,
            "expired": expired,
            "updated": updated,
            "nameservers": nameservers,
        }
    except Exception as e:
        return None

def format_hasil(data):
    ns = "\n".join([f"  • `{ns}`" for ns in data.get("nameservers", [])]) or "  • ?"
    return (
        f"🌐 *Whois Domain*\n\n"
        f"🔎 *Domain:* `{data['domain']}`\n"
        f"📋 *Status:* {data['status']}\n"
        f"📅 *Dibuat:* {data['dibuat']}\n"
        f"⏳ *Expired:* {data['expired']}\n"
        f"🔄 *Update:* {data['updated']}\n"
        f"🖥️ *Nameserver:*\n{ns}"
    )
