# Classical Piano Composer

This project is able to train model and output midi with polytonic pitch and velocity. By trial and error, it is found that using hidden layer LSTM 512 would cause the model training to get stuck at local minima with loss unable to get down to 1. By using hidden layer LSTM 256 and no dropout, the training model is able to get past local minima to achieve min loss.

Usage:
source classic_venv/bin/activate
python lstm.py
cp latest_weights to weights.hdf5
python predict.py
python testout.py
