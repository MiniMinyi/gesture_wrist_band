import flask
from flask import render_template, jsonify
import numpy as np
from io import StringIO
from PIL import Image
import requests
import socket
import base64
import json
import time
from data_container import Data_container

app = flask.Flask(__name__)
data_container = Data_container()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_image_1/<timestamp>', methods=['GET', 'POST'])
def get_image_1(timestamp):
    ret = requests.get("http://192.168.5.178/html/cam_pic.php/?time=%s&pDelay=40000" % timestamp)
    ret = ret.content
    data_container.insert_image(ret, 0)
    return ret


@app.route('/get_image_2/<timestamp>', methods=['GET', 'POST'])
def get_image_2(timestamp):
    ret = requests.get("http://192.168.5.73/html/cam_pic.php/?time=%s&pDelay=40000" % timestamp)
    ret = ret.content
    data_container.insert_image(ret, 1)
    return ret


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    status, rets_list, best_ret = data_container.predict()
    if best_ret in [2, 3, 4]:
        holo_ret = 4
    else:
        holo_ret = best_ret

    if status == 0:
        now = int(time.time() * 1000)
        try:
            sock.sendto(bytes("%d %d" % (now, holo_ret), "utf-8"), ("192.168.5.31", 12346))
        except Exception as e:
            pass
        return jsonify({"return_code": status, "rets_list": rets_list, "best_ret": best_ret})
    else:
        return jsonify({"return_code": status})


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8888)
