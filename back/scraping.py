import requests
import base64
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from safesearch import detect_safe_search

def images_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    detected_images = []

    p_img = re.compile(r"^.*\.(png|jpg|jpeg)$", re.IGNORECASE)

    for img in soup.find_all("img"):
        img_url = img.get("src")
        if not img_url:
            continue
        if not p_img.match(img_url):
            continue
        img_url = urljoin(url, img_url)
        detect_safe_search(img_url)
        img_content = requests.get(img_url).content
        encoded_bytes = base64.b64encode(img_content)
        detected_images.append(encoded_bytes.decode("utf-8"))

    return detected_images

if __name__ == "__main__":
    images_from_url("https://en.wikipedia.org/wiki/Hello")
