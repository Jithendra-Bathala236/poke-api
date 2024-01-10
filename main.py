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
    contentType = request.headers.get('Content-Type')

    if contentType != 'application/json':
        return json.dumps({
            "Message" : "Content Types isn't supported",
            "status" : False
            }), 400

    data = request.json
    id = pokemonCollection.count_documents({}) + 1
    data["id"] = id

    try:
        pokemonCollection.insert_one(data)
        return json.dumps({"Status": True, "Message": "Pokemon created successfully"}), 200
    except Exception as e:
        print(e)
        return json.dumps({"Status": False, "Message": "Unable to create Pokemon"}), 500

@app.route('/pokemon', methods=['GET'])
def getPokemon():

    id = request.args.get('id')

    if (id == None):
        pokemons = pokemonCollection.find({})
        data = []
        for pokemon in pokemons:
            pokemon["_id"] = str(pokemon["_id"])
            data.append(pokemon)
        return json.dumps({"Status": True, "Pokemons" : data, "Count": len(data)}), 200

    pokemon = pokemonCollection.find_one({"id": int(id)})

    if (pokemon):
        pokemon["_id"] = str(pokemon["_id"])
        return json.dumps({"Status": True, "Pokemon" : pokemon}), 200

    return json.dumps({"Message": "Pokemon not found", "Status" : False}), 404

@app.route('/pokemon/delete', methods=['DELETE'])
def deletePokemon():
    id = request.args.get('id')

    if (id == None):
        return json.dumps({"Status": False, "Message": "Invalid Pokemon Id"}), 400

    pokemon = pokemonCollection.delete_one({"id": int(id)})
    
    if (pokemon.deleted_count == 0):
        return json.dumps({"Message": "Pokemon not found", "Status" : False}), 404
    
    return json.dumps({"Message": "Pokemon Deleted Successfully", "Status": True}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8080)

