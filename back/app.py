# Back-end APIs will go here
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import random, json, re, datetime
import os
from threading import Lock

from scraping import images_from_url
from sensitive_content_detection import analyze_content, analyze_image

app = Flask(__name__)
app.secret_key = "gup4RzyNCNtgChRL"

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

dir_path = os.path.dirname(os.path.realpath(__file__))

log_mutex = Lock()

def log_event(type, message):
    with log_mutex:
        with open("./events.log", "a") as f:
            f.write("[{}] {}: {}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), type, message))

@app.route('/image', methods=["POST"])
@cross_origin()
def image_classify():
    log_event("INFO", "request image analysis")
    data = json.loads(request.data)
    if "image" not in data.keys():
        log_event("ERROR", "image not in request.data")
        return jsonify({
            "status": "error",
            "message": "The image was not correctly parsed."
        }), 400
    total_likelihood, potential_sensitive_content = [], []
    try:
        total_likelihood, potential_sensitive_content = analyze_image(data['image'][23:])
    except Exception as e:
        log_event("ERROR", str(e))
        return jsonify({
            "status": "error",
            "message": "There was a server error."
        }), 500
    if len(total_likelihood) != 3 and len(potential_sensitive_content) != 3:
        log_event("ERROR", "invalid length from google api")
        return jsonify({
            "status": "error",
            "message": "There was a server error."
        }), 500
    log_event("SUCCESS", "the image analysis succeeded")
    return jsonify({
        "status": "success",
        "data": {
            "adult": {
                "percentage": total_likelihood[0] * 100,
                "amount": potential_sensitive_content[0]
            },
            "medical": {
                "percentage": total_likelihood[1] * 100,
                "amount": potential_sensitive_content[1]
            },
            "violent": {
                "percentage": total_likelihood[2] * 100,
                "amount": potential_sensitive_content[2]
            },
        }
    }), 200

    
@app.route('/url', methods=["POST"])
@cross_origin()
def url_classify():
    log_event("INFO", "request url analysis")
    data = json.loads(request.data)
    if "url" not in data.keys():
        log_event("ERROR", "url not in request.data")
        return jsonify({
            "status": "error",
            "message": "The url was not correctly parsed." 
        }), 400
    else:
        if data["url"][:4] != "http":
            data["url"] = "http://" + data["url"]
        p = re.compile(r"^http(?:s)?:\/\/[a-zA-Z0-9\.]+\..{1,3}(?=\/|)")

        if not p.match(data["url"]):
            log_event("ERROR", "url not matched with regex")
            return jsonify({
                "status": "error",
                "message": "The url is invalid."
            }), 400
    images = []
    try:
        images = images_from_url(data["url"])
    except Exception as e:
        log_event("ERROR", str(e))
        return jsonify({
            "status": "error",
            "message": "There was a server error."
        }), 500
    if images == []:
        log_event("ERROR", "url does not contain images")
        return jsonify({
            "status": "error",
            "message": "No images were detected in the provided URL."
        }), 400
    total_likelihood, potential_sensitive_content = [], []
    try:
        total_likelihood, potential_sensitive_content = analyze_content(images)
    except Exception as e:
        log_event("ERROR", str(e))
        return jsonify({
            "status": "error",
            "message": "There was a server error."
        }), 500
    if len(total_likelihood) != 3 and len(potential_sensitive_content) != 3:
        log_event("ERROR", "invalid length from google api")
        return jsonify({
            "status": "error",
            "message": "There was a server error."
        }), 500
    log_event("SUCCESS", "the url analysis succeeded")
    return jsonify({
        "status": "success",
        "image_count": len(images),
        "data": {
            "adult": {
                "percentage": total_likelihood[0] * 100,
                "amount": potential_sensitive_content[0]
            },
            "medical": {
                "percentage": total_likelihood[1] * 100,
                "amount": potential_sensitive_content[1]
            },
            "violent": {
                "percentage": total_likelihood[2] * 100,
                "amount": potential_sensitive_content[2]
            },
        }
    }), 200
    

@app.errorhandler(404)
@cross_origin()
def page_not_found(error):
    return jsonify({
        "status": "error",
        "message": "The specified route does not exist."
    }), 404

if __name__ == "__main__":
    app.run(debug=True, threaded=True)