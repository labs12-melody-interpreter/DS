from flask import Flask, render_template, request, url_for, flash, redirect, send_file, Response
import pickle
import numpy as np
import json
from lstm import train_network, get_notes
from predict import generate
import os
from flask_cors import CORS, cross_origin


os.environ['KMP_DUPLICATE_LIB_OK']='True'
application = Flask(__name__)
CORS(application, resources=r"*")

application.config["DEBUG"] = True


@application.route('/', methods=['GET',"POST"])
def home():
    
    return render_template('home.html')

@application.route('/generator/', methods = ['POST', 'OPTIONS'])
@cross_origin(origin='*')
def music_generator():
    
    attempted_artist = request.json['artist']
    attempted_style = request.json['style']
    attempted_model = request.json['model']

    attempted_artist = attempted_artist.lower()
  
    notes = get_notes(attempted_artist, attempted_style)
    generate(notes, attempted_artist, attempted_style, attempted_model)
    
    return send_file('test_output.mid', mimetype='audio/midi', as_attachment=True)

if __name__ == "__main__":
    application.run(debug=True, threaded=True)