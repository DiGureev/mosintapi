import os
from flask import Flask
import json

app = Flask(__name__)

@app.route("/<email>")

def home(email):
    data = {}
    os.system(f"go run main.go {email} --output string")
    with open('./string', 'r') as f:
        data = json.load(f)
        del data['breachdirectory']
        del data['dns_records']
        
    return data, 200

if __name__ == "__main__":
    app.run(debug=True)





