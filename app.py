from flask import Flask, render_template, request, url_for, flash, redirect, send_file
import glob
import pickle
import numpy as np
import json
from music21 import converter, instrument, note, chord, stream
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from lstm import train_network, get_notes
from predict import generate
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'
app = Flask(__name__)
app.config["DEBUG"] = True


'''
def get_model():
    global model
    model = load_model ('.h5')
    print(" * Model loaded!")
'''



@app.route('/', methods=['GET',"POST"])
def home():
    try:
        if request.method == "POST":
            attempted_note = request.form['note']
            attempted_artist = request.form['artists']
            attempted_style = request.form['style']
            
            notes, n_vocab, model = train_network(attempted_artist, attempted_style)

    except Exception as e:
        flash(e)
        return render_template('home.html')

    return render_template('home.html')

@app.route('/generator/', methods = ['POST'])
def music_generator():
    attempted_note = request.form['note']
    attempted_artist = request.values['Artists']
    attempted_style = request.values['style']
    
    #notes = get_notes(attempted_artist, attempted_style)
    #generate(notes, Note = attempted_note)

    #print(attempted_note, attempted_artist, attempted_style)
    #return attempted_note, attempted_artist, attempted_style
    return send_file('test_output.mid', mimetype='audio/midi')

if __name__ == "__main__":
    app.run(debug=True)