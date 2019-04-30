from flask import Flask, render_template, request


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/predict/', methods = ['POST'])
def music_generator():
    pass


app.run(debug=True)