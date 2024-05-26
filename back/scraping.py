import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def images_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    img_urls = []

    p_img = re.compile(r"^.*\.(png|jpg|jpeg)$", re.IGNORECASE)

    for img in soup.find_all("img"):
        img_url = img.get("src")
        if not img_url:
            continue
        if not p_img.match(img_url):
            continue

        img_urls.append(urljoin(url, img_url))

    print(f"Se encontraron {len(img_urls)} imágenes en la página web.")

    return img_urls

    
