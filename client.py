import requests

# URL of the Flask server
BASE_URL = 'http://127.0.0.1:5000'

#send a GET request to the server. 
response = requests.get(BASE_URL)
print(response.text) # client is receiving data from server 




#send a POST request to the server.
data = {"name": "Alice", "age": 25}

response = requests.post(BASE_URL, json=data)

print(response.text) #printing the server's response 


