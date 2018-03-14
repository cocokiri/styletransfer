from __future__ import division, print_function

# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from tornado.web import Application, RequestHandler, stream_request_body
from tornado.ioloop import IOLoop
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

logging.basicConfig(filename='log.txt',level=logging.INFO)

TEMPLATE_PATH  = 'template.txt'
JS_PATH        = 'style.js'
STYLECODE_PATH = '/home/drwho/projects/style/playground/'

CHECKPOINTS  = ['models/relu5_1', 'models/relu4_1', 'models/relu3_1', 'models/relu2_1', 'models/relu1_1']
RELU_TARGETS = ['relu5_1', 'relu4_1', 'relu3_1', 'relu2_1', 'relu1_1']
VGG_PATH     = 'models/vgg_normalised.t7'
DEVICE       = '/gpu:0'
PATCH_SIZE   = 3
STRIDE       = 1

# init style model
# Load the WCT model
wct_model = WCT(checkpoints=CHECKPOINTS,
                relu_targets=RELU_TARGETS,
                vgg_path=VGG_PATH,
                device=DEVICE,
                ss_patch_size=PATCH_SIZE,
                ss_stride=STRIDE)

@stream_request_body
class UploadHandler(RequestHandler):
    def prepare(self):
        self.value = ValueTarget()
        self.file_ = FileTarget('/tmp/styleimg.jpg')
        self._parser = StreamingFormDataParser(headers=self.request.headers)
        self._parser.register('name', self.value)
        self._parser.register('file', self.file_)

    def data_received(self, chunk):
        self._parser.data_received(chunk)

    def post(self):
        img = self.request.files['image'][0]
        print(img['filename'])
        output_file = open("/tmp/" + img['filename'], 'w')
        output_file.write(img['body'])

class IndexHandler(RequestHandler):
    def get(self):
        # call style transfer
        mopa = STYLECODE_PATH + "models/"
        style_size = 256
        keep_colors = False
        alpha = 0.8
        style_path = STYLECODE_PATH + "images/style/shipwreck.jpg"
        content_path = STYLECODE_PATH + "images/content/golden_gate.jpg"
        out_path = STYLECODE_PATH + "images/results/"

        style_prefix = os.path.basename(style_path)  # Extract filename prefix without ext
        style_img = get_img_crop(style_path, resize=style_size)

        if style_size > 0:
            style_img = resize_to(style_img, style_size)
        
        content_img = get_img(content_path)
        if keep_colors:
            style_img = preserve_colors_np(style_img, content_img)

        # Run the frame through the style network
        stylized_rgb = wct_model.predict(content_img, style_img, alpha, False, 0.6, False)

        # Format for out filename: {out_path}/{content_prefix}_{style_prefix}.{content_ext}
        out_f = out_path + "test.jpg"
        # out_f = f'{content_prefix}_{style_prefix}.{content_ext}'
        save_img(out_f, stylized_rgb)

        #os.system(STYLECODE_PATH + "stylize.py " + "--checkpoints " + mopa + " relu5_1 " + mopa + " relu4_1 " + mopa + " relu3_1 " + 
        #          mopa + " relu2_1 " + mopa + " relu1_1 " + " --relu-targets relu5_1 relu4_1 relu3_1 relu2_1 relu1_1 " +
        #          " --style-size " + style_size + " --alpha " + alpha + " --style_path " + style_path) 

        # serve template
        self.render(TEMPLATE_PATH)

class JavascriptHandler(RequestHandler):
    def get(self):
        self.render(JS_PATH)

def main():
    handlers = [
        (r'/', IndexHandler),
        (r'/upload', UploadHandler),
        (r'/javascript', JavascriptHandler),
    ]

    settings = dict(
        debug=False,
        template_path=os.path.dirname(__file__)
    )

    app = Application(handlers, **settings)
    app.listen(8080)

    IOLoop().current().start()


if __name__ == "__main__":
    main()
