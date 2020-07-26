from main import motif

import flask
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
@cross_origin()
def general():
    svg = motif(600, 600, 8)
    response = flask.jsonify({'svg': svg})
    return response

@app.route("/<path:fullurl>", methods=['GET'])
@cross_origin()
def main(fullurl):

    height, width, n = [int(e) for e in fullurl.split('/')]
    svg = motif(height, width, n)
    response = flask.jsonify({'svg': svg})
    return response
