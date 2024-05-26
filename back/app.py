# Back-end APIs will go here
from flask import Flask, jsonify, request
import random, json, re, time
import os
from flask_cors import CORS, cross_origin

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
    op = random.choices([0, 1], weights=[0.2, 0.8])
    print(op)
    if op[0] == 1:
        return jsonify({
            "status": "success",
            "data": {
                "gore": {
                    "percentage": 0.06,
                    "amount": 1,
                },
                "violent": {
                    "percentage": 0,
                    "amount": 0,
                },
                "medical": {
                    "percentage": 0.26,
                    "amount": 16,
                },
                "adult": {
                    "percentage": 0.2,
                    "amount": 12,
                },
            },
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "There was a server error."
        }), 500

@app.errorhandler(404)
@cross_origin()
def page_not_found(error):
    return jsonify({
        "status": "error",
        "message": "The specified route does not exist."
    }), 404

if __name__ == "__main__":
    app.run(debug=True)