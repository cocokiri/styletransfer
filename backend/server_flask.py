from __future__ import division, print_function

from flask import Flask, Response, send_from_directory, request, send_file, jsonify
from flask_cors import CORS

import logging
import cgi
import os
import argparse
import numpy as np
import tensorflow as tf
from utils import preserve_colors_np
from utils import get_files, get_img, get_img_crop, save_img, resize_to, center_crop
import scipy
import time
from wct import WCT

logging.basicConfig(filename='log.txt', level=logging.INFO)

TEMPLATE_PATH  = 'template.html'
STYLECODE_PATH = '/home/drwho/projects/style/playground/'
STATIC_PATH    = STYLECODE_PATH + 'backend/static/'
BACKEND_PATH   = STYLECODE_PATH + 'backend/'
CONTENT_IMG_PATH = STYLECODE_PATH + 'backend/static/images/content/'
STYLE_IMG_PATH = STYLECODE_PATH + 'backend/static/images/style/'

CHECKPOINTS  = ['models/relu5_1', 'models/relu4_1', 'models/relu3_1', 'models/relu2_1', 'models/relu1_1']
RELU_TARGETS = ['relu5_1', 'relu4_1', 'relu3_1', 'relu2_1', 'relu1_1']
VGG_PATH     = 'models/vgg_normalised.t7'
DEVICE       = '/gpu:0'
PATCH_SIZE   = 3
STRIDE       = 1

# init flask
app = Flask(__name__, static_url_path='/static', static_folder=STATIC_PATH)
CORS(app)

wct_model = None

@app.route("/upload_content", methods=['POST'])
def post_content():
    f = request.files['content_img']
    myid = str(int(time.time()*10000) + ".jpg")
    f.save(CONTENT_IMG_PATH + myid)
    print("+ new content image " + myid)
    return Response("{'content_img_url':'" + myid + "'}", status=200, mimetype='application/json')

@app.route("/upload_style", methods=['POST'])
def post_style():
    f = request.files['style_img']
    myid = str(int(time.time()*10000) + ".jpg")
    f.save(STYLE_IMG_PATH + myid)
    print("+ new style image " + myid)
    return Response("{'style_img_url':'" + myid + "'}", status=200, mimetype='application/json')

@app.route("/stylize", methods=['POST'])
def post_params():
    myid = str(int(time.time()*10000) + ".jpg")
    tmp_img_post_path = '/tmp/styled_img_' + myid
    
    content_img_url = CONTENT_IMG_PATH + request.form['content_img_url']
    alpha = request.form['alpha']
    content_img = get_img(content_img_url)
    style_size = request.form['style_scale'] * 512
    print(content_img.shape)

    # style_img = get_img_crop(style_img_url, resize=style_size)
    style_img = get_img_crop(style_img_url)

    if style_size > 0:
        style_img = resize_to(style_img, style_size)

    if keep_colors:
        style_img = preserve_colors_np(style_img, content_img)

    # Run the frame through the style network
    stylized_rgb = wct_model.predict(content_img, style_img, alpha, False, 0.6, False)

    save_img(tmp_img_post_path, stylized_rgb)
    return send_file(tmp_img_post_path)

@app.route("/")
def get_index():
    # serve template
    return send_from_directory(BACKEND_PATH, TEMPLATE_PATH)

@app.route("/get_content_images")
def get_content_images():
    fli = os.listdir(CONTENT_IMG_PATH)
    return jsonify(fli)

@app.route("/get_style_images")
def get_style_images():
    fli = os.listdir(STYLE_IMG_PATH)
    return jsonify(fli)

def main():
    # init style model
    # Load the WCT model
    global wct_model
    if wct_model is None:
        wct_model = WCT(checkpoints=["".join([BACKEND_PATH,chkp]) for chkp in CHECKPOINTS],
                    relu_targets=RELU_TARGETS,
                    vgg_path=BACKEND_PATH+VGG_PATH,
                    device=DEVICE,
                    ss_patch_size=PATCH_SIZE,
                    ss_stride=STRIDE)
    app.run(host='0.0.0.0',debug=False,port=8080)
    
if __name__ == "__main__":
    main()

