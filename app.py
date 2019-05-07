from flask import Flask, render_template, request, url_for, flash, redirect, send_file, Response
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
from keras import backend as K
from lstm import train_network, get_notes
from predict import generate
import os
from flask_cors import CORS, cross_origin
from midiutil import MIDIFile
import io


os.environ['KMP_DUPLICATE_LIB_OK']='True'
app = Flask(__name__)
CORS(app, support_credentials=True, send_wildcard = True, resources={r"/*": {"origins": ["http://localhost:3000", "https://elegant-knuth-1dc044.netlify.com/"]}})


app.config["DEBUG"] = True


'''
def get_model():
    global model
    model = load_model ('.h5')
    print(" * Model loaded!")
'''
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    # use str instead of basestring if using Python 3.x
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    # use str instead of basestring if using Python 3.x
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


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
    
    attempted_artist = attempted_artist.lower()

    notes = get_notes(attempted_artist, attempted_style)
    generate(notes, attempted_note, attempted_artist, attempted_style)

    K.clear_session()
    
    #print(attempted_note, attempted_artist, attempted_style)
    #return attempted_note
    
  
    return send_file('test_output.mid', mimetype='audio/midi', as_attachment=True).headers.add('Access-Control-Allow-Origin', '*')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)