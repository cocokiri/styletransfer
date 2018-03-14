from __future__ import division, print_function

from flask import Flask, send_from_directory, request, send_file
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
JS_PATH        = 'style.js'
STYLECODE_PATH = '/home/drwho/projects/style/playground/'
BACKEND_PATH   = STYLECODE_PATH + 'backend/'

CHECKPOINTS  = ['models/relu5_1', 'models/relu4_1', 'models/relu3_1', 'models/relu2_1', 'models/relu1_1']
RELU_TARGETS = ['relu5_1', 'relu4_1', 'relu3_1', 'relu2_1', 'relu1_1']
VGG_PATH     = 'models/vgg_normalised.t7'
DEVICE       = '/gpu:0'
PATCH_SIZE   = 3
STRIDE       = 1

# init flask
app = Flask(__name__)
CORS(app)

wct_model = None

@app.route("/upload", methods=['POST'])
def post():
    tmp_img_path = '/tmp/style_img_input.jpg'
    tmp_img_post_path = '/tmp/style_img_styled.jpg'
    f = request.files['content_img']
    f.save(tmp_img_path)
    mopa = BACKEND_PATH + "models/"
    style_size = 256
    keep_colors = False
    alpha = 0.8
    style_path = STYLECODE_PATH + "images/style/shipwreck.jpg"
    out_path = STYLECODE_PATH + "images/results/"

    style_prefix = os.path.basename(style_path)  # Extract filename prefix without ext
    style_img = get_img_crop(style_path, resize=style_size)

    if style_size > 0:
        style_img = resize_to(style_img, style_size)

    content_img = get_img(tmp_img_path)
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

@app.route("/javascript")
def get_js():
    return send_from_directory(BACKEND_PATH, JS_PATH)

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

