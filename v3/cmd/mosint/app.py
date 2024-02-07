import subprocess
import os
from flask import Flask
import json

#to get results we need to add API keys in .mosint.yaml file in the root dir

app = Flask(__name__)

@app.route("/<email>")

def home(email):
    data = {}

    emailname = email.replace(".", "_")

    if os.path.exists(f"./{emailname}.json"):
        print("Exists")
        with open(f"./{emailname}.json","r") as f:
            data = json.load(f)
    else:
        print("Does not Exist")
        # Execute the command that creates a string.json file with results
        subprocess.run(['./main', f'{email}', '--config', '/etc/secrets/.mosint.yaml', '--output', 'string'], check=True)

        #open that json file
        with open('./string', 'r') as f:
            data = json.load(f)
            #delete keys which contain info we don't care about
            if "breachdirectory" in data:
                del data['breachdirectory']
                del data['dns_records']

        with open(f"./{emailname}.json", "w") as f:
                json.dump(data, f)

    #return result in json    
    return data, 200

if __name__ == "__main__":
    app.run(debug=True)





