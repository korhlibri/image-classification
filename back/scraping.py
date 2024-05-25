import requests, base64, re
from bs4 import BeautifulSoup

def images_from_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    detected_images = []

    p_url = re.compile(r"^http(?:s)?:\/\/.+?(?=\/)")
    base_url = p_url.search(url).group(0)

    p_img = re.compile(r"^.*\.(png|jpg|jpeg)(?= |\n)*$")

    for img in soup.find_all("img"):
        img_url = img["src"]
        if not p_img.match(img_url):
            continue
        if not p_url.match(img_url):
            img_url = base_url + img_url
        img_content = requests.get(img_url).content
        encoded_bytes = base64.b64encode(img_content)
        detected_images.append(encoded_bytes.decode("utf-8"))

    return detected_images

if __name__ == "__main__":
    print(images_from_url("https://en.wikipedia.org/wiki/Hello"))