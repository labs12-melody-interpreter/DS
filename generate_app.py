import base64import 
import numpy as np
import io
from PIL import Image
from keras.models import Sequential
from keras.models import load_model
from keras.models import model_fromjson
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from flask import request
from flask import jsonify
from flask import Flask

app = Flask(__name__)

def get_model():
    global model
    model = load_model ('.h5')
    print(" * Model loaded!")


print(" * Loading Keras model...")
get_model()

@app.route("/generate", methods=["POST"])
def generate():
    message = request.get_json(force=True)
    note = message['note']
    if note in dictionary:
        print(" * Note is in dictionary!")
        
    
    
