


import os  
import json
import jwt
from flask import Flask, render_template, request, jsonify
import urllib.request
import io

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

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
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text


# function to check the file extension
def allowed_file(filename):  
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# route and function to handle the upload page
@app.route('/', methods=['GET', 'POST'])
def upload_page():  
    if request.method == 'POST':
        # get the image URL
        img_url = request.form.get('img_url')
        if img_url is None:
            return jsonify({'error': 'No URL selected'})
        
        # download the image from the URL
        img = urllib.request.urlopen(img_url)
        file = io.BytesIO(img.read())

        if file and allowed_file(img_url):
            # call the OCR function on it
            extracted_text = ocr_core(file)

            # extract the text and display it
            return jsonify({'message': 'Successfully processed',
                            'extracted_text': extracted_text,
                            'img_src': img_url})
    elif request.method == 'GET':
        return ""


if __name__ == '__main__':  
    app.run(debug = True , port = 5000)
