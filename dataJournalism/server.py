# flask --app data_server run
from flask import Flask
from flask import render_template
from flask import request
import json
import math

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def about():
    #f = open("dataJournalism/data/math_scores.json")
    #data = json.load(f)
    #f.close()
    
    #print(data)

    return render_template('about.html')


app.run(debug=True)