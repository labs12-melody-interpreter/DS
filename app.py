from flask import Flask, render_template, request, url_for, flash, redirect, send_file, Response
import pickle
import numpy as np
import json
'''
from music21 import converter, instrument, note, chord, stream

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
'''
from keras import backend as K

from lstm import train_network, get_notes
from predict import generate
import os
from flask_cors import CORS, cross_origin

os.environ['KMP_DUPLICATE_LIB_OK']='True'
app = Flask(__name__)
CORS(app, resources=r"*")





app.config["DEBUG"] = True



@app.route('/', methods=['GET',"POST"])
def home():

    return render_template('home.html')

@app.route('/generator/', methods = ['POST', 'OPTIONS'])
@cross_origin(origin='*')
def music_generator():
    
    K.clear_session()

    attempted_note = request.json['note']
    attempted_artist = request.json['artist']
    attempted_style = request.json['style']
    attempted_model = request.json['model']

    attempted_artist = attempted_artist.lower()

    notes = get_notes(attempted_artist, attempted_style)
    generate(notes, attempted_note, attempted_artist, attempted_style, attempted_model)

    K.clear_session()
    
    #print(attempted_note, attempted_artist, attempted_style)
    #return attempted_note
    
  
    return send_file('test_output.mid', mimetype='audio/midi', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)