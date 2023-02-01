import os  
import json
import jwt
from flask import Flask, render_template, request, jsonify


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

def authenticate(request):
    """
    Authenticate the request using JWT.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        return False
    try:
        data = jwt.decode(auth_token,  algorithms=['HS256'])
    except:
        return False
    return True

# route and function to handle the upload page
# route and function to handle the upload page
@app.route('/', methods=['GET', 'POST'])
def upload_page():  
    if request.method == 'POST':
        # check if there is an API key in the request
        if 'api_key' not in request.form:
            return jsonify({'error': 'No API Key provided...'})
        api_key = request.form['api_key']
        # validate the API key
        if api_key != '2fzdg5lauxlbh7k9m8n6pqrs3uvwbyz01':
            return jsonify({'error': 'Invalid API Key'})
        
        # check if there is a file in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'})
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'})

        if file and allowed_file(file.filename):
            # call the OCR function on it
            extracted_text = ocr_core(file)

            # extract the text and display it
            return jsonify({'message': 'Successfully processed',
                            'extracted_text': extracted_text,
                            'img_src': UPLOAD_FOLDER + file.filename})
    elif request.method == 'GET':
        return render_template('upload.html')
    else:
        pass


if __name__ == '__main__':  
    app.run(debug = True , port = 5000)






