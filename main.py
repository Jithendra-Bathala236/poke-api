from flask import Flask, request
from pymongo import MongoClient
import json

app = Flask(__name__)

uri = "mongodb+srv://jithendrabathala:pass123@cluster0.rbyrwgz.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(uri)['poke-api']
    print("Successfully connected to Mongo")
except Exception as e:
    print(e)
    raise e

pokemonCollection = client['pokemons']

@app.route('/')
def hello():
    return json.dumps({"Status": True, "Message": "API is successful running"})

@app.route('/pokemon/create', methods=['POST'])
def createPokemon():
    if request.method != 'POST':
        return json.dumps({"Status": False, "Message": "url not found"}), 404
    
    contentType = request.headers.get('Content-Type')

    if contentType != 'application/json':
        return json.dumps({
            "Message" : "Content Types isn't supported",
            "status" : False
            }), 400

    data = request.json
    try:
        pokemonCollection.insert_one(data)
        return json.dumps({"Status": True, "Message": "Pokemon created successfully"}), 200
    except Exception as e:
        print(e)
        return json.dumps({"Status": False, "Message": "Unable to create Pokemon"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8080)

