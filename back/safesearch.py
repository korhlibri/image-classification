import argparse
from google.cloud import vision

def detect_safe_search(uri):
    """Detects unsafe features in the file."""

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
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

    if likelihood_name[safe.adult] == "UNKNOWN":
        print("\n***************************************\n")
        print(
            f" Image with uri:\n {uri} \n could not be processed"
        )
        print("\n***************************************\n")
        return
    
    print("\n***************************************\n")
    print(f"Image from {uri}:")
    print(f"adult: {likelihood_name[safe.adult]}")
    print(f"medical: {likelihood_name[safe.medical]}")
    print(f"violence: {likelihood_name[safe.violence]}")
    print("\n***************************************\n")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
