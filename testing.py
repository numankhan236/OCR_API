

import requests

url = "http://127.0.0.1:5000"

# specify the URL of the image you want to process
img_url = "https://cdn.pixabay.com/photo/2016/11/18/14/59/image-1835151_960_720.jpg"

# send the post request to the API endpoint with the image URL
response = requests.post(url, data={"url": img_url})

# check if the request was successful
if response.status_code == 200:
    # parse the JSON response from the server
    result = response.json()
    print(result)

    # # extract the extracted text from the response
    # extracted_text = result["extracted_text"]
    # print("Extracted text:", extracted_text)
else:
    # there was an error in the request
    print("Request failed:", response.content)

