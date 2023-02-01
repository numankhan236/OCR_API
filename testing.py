import requests

url = "http://localhost:5000/"

api_key = "2fzdg5lauxlbh7k9m8n6pqrs3uvwbyz01"

image_file = {'file': ('.\static\S3.PNG', open('.\static\S3.PNG', 'rb'))}
second_image = {'file': ('.\static\Capture2.PNG', open('.\static\Capture2.PNG', 'rb'))}
response = requests.post(url, data={'api_key': api_key}, files=second_image)

print(response.json())
