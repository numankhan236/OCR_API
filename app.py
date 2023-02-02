


import os  
import json
import jwt
from flask import Flask, render_template, request, jsonify
import urllib.request
import io
from paddleocr import PaddleOCR, draw_ocr
import numpy as np

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

ocr = PaddleOCR(use_angle_cls=True, lang='en')

# secret key to encode and decode the JWT
# SECRET_KEY = "YOUR_SECRET_KEY"

def ocr_core(filename):  
    """
    This function will handle the core OCR processing of images.
    """
    try:  
        from PIL import Image
    except ImportError:  
        import Image

    img_ = Image.open(filename).convert('RGB')
    image_ = np.array(img_)  # convert image to numpy array for ocr
    result = ocr.ocr(image_, cls=True)
    return result
    


# function to check the file extension
def allowed_file(filename):  
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# route and function to handle the upload page
@app.route('/', methods=['GET', 'POST'])
def upload_page():  
    if request.method == 'POST':
        # get the image URL
        # img_url = request.form.get('img_url')     # this will get it from form data
        req = request.get_json()                    # this will get it from raw form data
        img_url = req['img_url']
        if img_url is None:
            return jsonify({'error': 'No URL selected'})
        
        # download the image from the URL
        img = urllib.request.urlopen(img_url)
        file = io.BytesIO(img.read())

        if file and allowed_file(img_url):
            # call the OCR function on it
            extracted_text = ocr_core(file)

            texts = [line[1][0] for line in extracted_text[0]]
            lang_url = './AAntiCorona-L3Ax3.ttf'

            # extract the text and display it
            return jsonify({'message': 'Successfully processed',
                            'extracted_text': texts,
                            'img_src': img_url})
    elif request.method == 'GET':
        return ""


if __name__ == '__main__':  
    app.run(debug = True , port = 5000)
