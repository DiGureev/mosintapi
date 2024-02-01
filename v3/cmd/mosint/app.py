import os
import subprocess
from flask import Flask
import json

#to get results we need to add API keys in .mosint.yaml file in the root dir

app = Flask(__name__)

@app.route("/<email>")

def home(email):
    data = {}

    # # Define the path to your Go executable
    # go_script_path = './main.exe'

    # # Optionally, add arguments
    # args = f'{email} --output string'

    # # Construct the command
    # command = f'{go_script_path} {args}'

    # # Execute the command
    subprocess.run(f'./main.exe {email} --output string')

    #call the go-script (main.go) from CLI with parametr that creates a string.json file with results
    # os.system(f"go run main.go {email} --output string")
    #open that json file
    with open('./string', 'r') as f:
        data = json.load(f)
        #delete keys which contain info that we don't care about
        del data['breachdirectory']
        del data['dns_records']
        
    #return result in json    
    return data, 200

if __name__ == "__main__":
    app.run(debug=True)





