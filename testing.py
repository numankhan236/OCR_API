import requests

url = "http://localhost:5000/"


image_file = {'file': ('S3.PNG', open('S3.PNG', 'rb'))}
second_image = {'file': ('.\static\Capture2.PNG', open('.\static\Capture2.PNG', 'rb'))}
response = requests.post(url,  files=second_image)

print(response.json())