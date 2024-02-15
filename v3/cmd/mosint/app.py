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

    if os.path.exists(f"./reports/{emailname}.json"):
        print("Exists")
        with open(f"./reports/{emailname}.json","r") as f:
            data = json.load(f)

    else:
        print("Does not Exist")
        # Execute the command that creates a string.json file with results
        subprocess.run(['./main', f'{email}', '--config', '/etc/secrets/.mosint.yaml', '--output', 'string'], check=True)
        
        # For testing locally:
        # os.system(f'go run /Users/Diana/Desktop/mosintapi/v3/cmd/mosint/main.go {email} --config /Users/Diana/Desktop/mosintapi/.mosint.yaml --output string')

        # open that json file
        with open('./string', 'r') as f:
            data = json.load(f)
            #delete keys which contain info we don't care about
            if "breachdirectory" in data:
                del data['breachdirectory']
                del data['dns_records']

        with open(f"./reports/{emailname}.json", "w") as f:
                json.dump(data, f)

    #return result in json    
    
    cleandata = {}

    cleandata["email"] = data["email"]
    cleandata["verified"] = data["verified"]
    cleandata["blacklisted"] = data["emailrep"]["details"]["blacklisted"]
    cleandata["age"] = data["emailrep"]["details"]["days_since_domain_creation"]
    cleandata["spam"] = data["emailrep"]["details"]["spam"]
    cleandata["suspicious"] = data["emailrep"]["suspicious"]
    cleandata["websites"] = {}
    cleandata["websites"]["google_search"] = data["google_search"]
    cleandata["websites"]["instagram"] = data["instagram_exists"]
    cleandata["websites"]["spotify"] = data["spotify_exists"]
    cleandata["websites"]["twitter"] = data["twitter_exists"]
    cleandata["data"] = data["hunter"]["data"]

    print(cleandata)

    return cleandata, 200

if __name__ == "__main__":
    app.run(debug=True)





