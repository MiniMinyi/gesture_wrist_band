import flask
from flask import render_template, jsonify
import numpy as np
from io import StringIO
from PIL import Image
import requests
import base64
from data_container import Data_container

app = flask.Flask(__name__)
data_container = Data_container()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_image_1/<timestamp>', methods=['GET', 'POST'])
def get_image_1(timestamp):
    ret = requests.get("http://10.19.218.9/html/cam_pic.php/?time=%s&pDelay=40000" % timestamp)
    ret = ret.content
    data_container.insert_image(ret, 0)
    return ret


@app.route('/get_image_2/<timestamp>', methods=['GET', 'POST'])
def get_image_2(timestamp):
    ret = requests.get("http://10.18.169.208/html/cam_pic.php/?time=%s&pDelay=40000" % timestamp)
    ret = ret.content
    data_container.insert_image(ret, 1)
    return ret


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    status, ret = data_container.predict()
    if status == 0:
        return jsonify({"return_code": status, "ret": ret})
    else:
        return jsonify({"return_code": status})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)
