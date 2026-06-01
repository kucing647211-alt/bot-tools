import random
import string

NAMA_DEPAN = [
    "Andi", "Budi", "Citra", "Dian", "Eka", "Fajar", "Gita", "Hendra",
    "Indah", "Joko", "Kartika", "Lina", "Made", "Nadia", "Omar", "Putri",
    "Reza", "Sari", "Toni", "Umar", "Vina", "Wahyu", "Xena", "Yanti", "Zaki"
]

NAMA_BELAKANG = [
    "Santoso", "Wijaya", "Kusuma", "Pratama", "Suharto", "Rahayu",
    "Hidayat", "Nugroho", "Susanto", "Wibowo", "Hartono", "Gunawan",
    "Setiawan", "Purnomo", "Saputra", "Mahendra", "Utama", "Firmansyah"
]

KOTA = [
    "Jakarta", "Surabaya", "Bandung", "Medan", "Semarang",
    "Makassar", "Palembang", "Tangerang", "Depok", "Bekasi",
    "Bogor", "Yogyakarta", "Solo", "Malang", "Denpasar"
]

JALAN = [
    "Jl. Merdeka", "Jl. Sudirman", "Jl. Gatot Subroto", "Jl. Ahmad Yani",
    "Jl. Diponegoro", "Jl. Veteran", "Jl. Pahlawan", "Jl. Pemuda",
    "Jl. Mawar", "Jl. Melati", "Jl. Anggrek", "Jl. Kenanga"
]

DOMAIN_EMAIL = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]

PEKERJAAN = [
    "Programmer", "Desainer Grafis", "Guru", "Dokter", "Akuntan",
    "Marketing", "Fotografer", "Wirausaha", "Mahasiswa", "Freelancer"
]

def generate_identitas():
    """Generate identitas palsu/dummy untuk keperluan testing"""
    nama_depan = random.choice(NAMA_DEPAN)
    nama_belakang = random.choice(NAMA_BELAKANG)
    nama_lengkap = f"{nama_depan} {nama_belakang}"

    # Generate tanggal lahir
    tahun = random.randint(1980, 2000)
    bulan = random.randint(1, 12)
    hari = random.randint(1, 28)
    tgl_lahir = f"{hari:02d}/{bulan:02d}/{tahun}"

    # Generate nomor HP
    prefix = random.choice(["0812", "0813", "0821", "0822", "0851", "0852", "0857", "0858"])
    nomor_hp = prefix + ''.join(random.choices(string.digits, k=8))

    # Generate email
    angka = random.randint(10, 999)
    domain = random.choice(DOMAIN_EMAIL)
    email = f"{nama_depan.lower()}{nama_belakang.lower()}{angka}@{domain}"

    # Generate alamat
    kota = random.choice(KOTA)
    jalan = random.choice(JALAN)
    nomor_jalan = random.randint(1, 200)
    kodepos = ''.join(random.choices(string.digits, k=5))
    alamat = f"{jalan} No. {nomor_jalan}, {kota} {kodepos}"

    # Generate username
    username = f"{nama_depan.lower()}{angka}"

    # Pekerjaan
    pekerjaan = random.choice(PEKERJAAN)

    return {
        "nama": nama_lengkap,
        "tgl_lahir": tgl_lahir,
        "pekerjaan": pekerjaan,
        "email": email,
        "nomor_hp": nomor_hp,
        "alamat": alamat,
        "kota": kota,
        "username": username,
    }

def format_identitas(data):
    return (
        f"🎲 *Identitas Dummy*\n\n"
        f"👤 *Nama:* {data['nama']}\n"
        f"🎂 *Tgl Lahir:* {data['tgl_lahir']}\n"
        f"💼 *Pekerjaan:* {data['pekerjaan']}\n"
        f"📧 *Email:* `{data['email']}`\n"
        f"📱 *No. HP:* `{data['nomor_hp']}`\n"
        f"🏠 *Alamat:* {data['alamat']}\n"
        f"👾 *Username:* `{data['username']}`\n\n"
        f"⚠️ _Data ini fiktif, hanya untuk testing form/UI._"
    )
