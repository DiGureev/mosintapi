import os
from flask import Flask
import json

#to get results we need to add API keys in .mosint.yaml file in the root dir

app = Flask(__name__)

@app.route("/<email>")

def home(email):
    data = {}

    # Execute the command that creates a string.json file with results
    os.system('./main' f'{email}' '--config' '/etc/secrets/.mosint.yaml' '--output' 'string')

    #open that json file
    with open('./string', 'r') as f:
        data = json.load(f)
        #delete keys which contain info we don't care about
        if "breachdirectory" in data:
            del data['breachdirectory']
            del data['dns_records']
        
    #return result in json    
    return data, 200

if __name__ == "__main__":
    app.run(debug=True)





