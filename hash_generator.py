import hashlib

def generate_hash(teks):
    """Generate berbagai jenis hash dari teks"""
    encoded = teks.encode('utf-8')
    return {
        "MD5": hashlib.md5(encoded).hexdigest(),
        "SHA1": hashlib.sha1(encoded).hexdigest(),
        "SHA256": hashlib.sha256(encoded).hexdigest(),
        "SHA512": hashlib.sha512(encoded).hexdigest(),
    }

def format_hasil(teks, hasil):
    return (
        f"💻 *Hash Generator*\n\n"
        f"📝 *Input:* `{teks[:50]}{'...' if len(teks) > 50 else ''}`\n\n"
        f"🔐 *MD5:*\n`{hasil['MD5']}`\n\n"
        f"🔐 *SHA1:*\n`{hasil['SHA1']}`\n\n"
        f"🔐 *SHA256:*\n`{hasil['SHA256']}`\n\n"
        f"🔐 *SHA512:*\n`{hasil['SHA512'][:64]}...`\n\n"
        f"⚠️ _Hash tidak bisa di-decrypt, hanya untuk verifikasi data._"
    )
