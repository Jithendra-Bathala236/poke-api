from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return json.dumps({"Status": True, "Message": "API is successful running"})

if __name__ == '__main__':
    app.run(debug=True, port=8080)

