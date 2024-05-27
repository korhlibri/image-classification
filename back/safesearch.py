import argparse
import base64
import os
from google.cloud import vision
from google.oauth2 import service_account


def detect_safe_search_base64(base64_string):
    """Detects unsafe features in the file."""

    # Names of likelihood from google.cloud.vision.enums
    likelihood = (
        0,
        0.05,
        0.15,
        0.45,
        0.75,
        0.95,
    )

    client = vision.ImageAnnotatorClient()

     # Decode base64 string to bytes
    image_data = base64.b64decode(base64_string, validate=True)

    # Write locally the temporary image to be able to use it in the api
    temp_file = "temp.jpg"

    with open("temp.jpg", "wb") as f:
        f.write(image_data)

    # Open the file to read the contents
    with open("temp.jpg", "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)

    try:
        safe = response.safe_search_annotation
    except AttributeError:
        print("\n***************************************\n")
        print(
            f" The image could not be processed"
        )
        print("\n***************************************\n")
        return

    if likelihood[safe.adult] == "UNKNOWN":
        print("\n***************************************\n")
        print(
            f" The image could not be processed"
        )
        print("\n***************************************\n")
        return
    
    os.remove("temp.jpg")
        
    return [likelihood[safe.adult], likelihood[safe.medical], likelihood[safe.violence]]


def detect_safe_search_url(uri):
    """Detects unsafe features in the file."""

    # Names of likelihood from google.cloud.vision.enums
    likelihood = (
        0,
        0.05,
        0.15,
        0.45,
        0.75,
        0.95,
    )

    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = uri

    response = client.safe_search_detection(image=image)
    try:
        safe = response.safe_search_annotation 
    except AttributeError:
        print("\n***************************************\n")
        print(
            f" Image with uri:\n {uri} \n could not be processed"
        )
        print("\n***************************************\n")
        return

    if likelihood[safe.adult] == "UNKNOWN":
        print("\n***************************************\n")
        print(
            f" Image with uri:\n {uri} \n could not be processed"
        )
        print("\n***************************************\n")
        return
    
    return [likelihood[safe.adult], likelihood[safe.medical], likelihood[safe.violence]]    

