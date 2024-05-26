# Back-end APIs will go here
from flask import Flask, jsonify, request
import random, json, re, time
import os
from flask_cors import CORS, cross_origin

from scraping import images_from_url
from sensitive_content_detection import analyze_content

app = Flask(__name__)
app.secret_key = "gup4RzyNCNtgChRL"

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

dir_path = os.path.dirname(os.path.realpath(__file__))

@app.route('/image', methods=["POST"])
@cross_origin()
def image_classify():
    data = json.loads(request.data)
    if "image" not in data.keys():
        return jsonify({
            "status": "error",
            "message": "The image was not correctly parsed."
        }), 400
    op = random.choices([0, 1], weights=[0.2, 0.8])
    if op[0] == 1:
        return jsonify({
            "status": "success",
            "data": {
                "gore": 0.1,
                "violent": 0.25,
                "medical": 0.75,
                "adult": 0.2
            },
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "There was a server error."
        }), 500
    
@app.route('/url', methods=["POST"])
@cross_origin()
def url_classify():
    data = json.loads(request.data)
    if "url" not in data.keys():
        return jsonify({
            "status": "error",
            "message": "The url was not correctly parsed."
        }), 400
    else:
        if data["url"][:4] != "http":
            data["url"] = "http://" + data["url"]
        p = re.compile(r"^http(?:s)?:\/\/[a-zA-Z0-9\.]+\..{1,3}(?=\/|)")

        if not p.match(data["url"]):
            return jsonify({
                "status": "error",
                "message": "The url is invalid."
            }), 400
    images = []
    try:
        images = images_from_url(data["url"])
    except Exception as e:
        print(e)
        return jsonify({
            "status": "error",
            "message": "There was a server error."
        }), 500
    if images == []:
        return jsonify({
            "status": "error",
            "message": "No images were detected in the provided URL."
        }), 400
    total_likelihood, potential_sensitive_content = [], []
    try:
        total_likelihood, potential_sensitive_content = analyze_content(images)
    except Exception as e:
        print(e)
        return jsonify({
            "status": "error",
            "message": "There was a server error."
        }), 500
    if len(total_likelihood) != 3 and len(potential_sensitive_content) != 3:
        return jsonify({
            "status": "error",
            "message": "There was a server error."
        }), 500
    return jsonify({
        "status": "success",
        "data": {
            "adult": {
                "percentage": total_likelihood[0],
                "amount": potential_sensitive_content[0]
            },
            "medical": {
                "percentage": total_likelihood[1],
                "amount": potential_sensitive_content[1]
            },
            "violent": {
                "percentage": total_likelihood[2],
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
    app.run(debug=True)