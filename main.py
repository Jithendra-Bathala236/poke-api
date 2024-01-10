from flask import Flask
from pymongo import MongoClient
import json

app = Flask(__name__)

uri = "mongodb+srv://jithu:1234@cluster0.isqyov3.mongodb.net/?retryWrites=true&w=majority"

# client = ""

try:
    client = MongoClient(uri)['poke-api']
    print("Successfully connected to Mongo")
except Exception as e:
    print(e)
    raise e 

# print(client.list_collection_names())

@app.route('/')
def hello():
    return json.dumps({"Status": True, "Message": "API is successful running"})

if __name__ == '__main__':
    app.run(debug=True, port=8080)

