from flask import Flask, request, jsonify

app = Flask(__name__)
thisdir = pathlib.Path(__file__).parent.absolute() # path to directory of this file

@app.route('/', methods=['GET'])
def get_webpage():
	