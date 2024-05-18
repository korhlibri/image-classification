# Back-end APIs will go here
from flask import Flask, jsonify
import os

app = Flask(__name__)
app.secret_key = "gup4RzyNCNtgChRL"

dir_path = os.path.dirname(os.path.realpath(__file__))

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "status": "error",
        "message": "The specified route does not exist."
    }), 404

if __name__ == "__main__":
    app.run(debug=True)