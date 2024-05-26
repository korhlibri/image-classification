import argparse
from google.cloud import vision

def detect_safe_search(uri):
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

