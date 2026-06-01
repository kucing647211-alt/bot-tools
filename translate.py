from deep_translator import GoogleTranslator

BAHASA = {
    "id": "Indonesia",
    "en": "Inggris",
    "ja": "Jepang",
    "ko": "Korea",
    "zh-CN": "China",
    "ar": "Arab",
    "fr": "Prancis",
    "de": "Jerman",
    "es": "Spanyol",
    "ru": "Rusia",
}

def translate_teks(teks, bahasa_tujuan="en", bahasa_asal="auto"):
    """Terjemahkan teks ke bahasa tujuan"""
    try:
        result = GoogleTranslator(source=bahasa_asal, target=bahasa_tujuan).translate(teks)
        return result
    except Exception as e:
        return None

def daftar_bahasa():
    return BAHASA
