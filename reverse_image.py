import urllib.parse

def reverse_image_search(url_gambar):
    """Generate link reverse image search dari berbagai mesin pencari"""
    encoded = urllib.parse.quote(url_gambar, safe='')
    
    links = {
        "Google Images": f"https://www.google.com/searchbyimage?image_url={encoded}",
        "TinEye": f"https://tineye.com/search?url={encoded}",
        "Yandex": f"https://yandex.com/images/search?url={encoded}&rpt=imageview",
        "Bing": f"https://www.bing.com/images/search?view=detailv2&iss=sbi&q=imgurl:{encoded}",
    }
    return links
