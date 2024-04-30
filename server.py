from flask import *
import mqttSub
import pickle

app = Flask(__name__,
            static_url_path='',
            static_folder='webpage')

@app.route('/', methods=['GET'])
def homepage():
    return app.send_static_file('index.html')

@app.route('/sensor', methods=['GET'])
def get_data():
    data = ""
    with open('data/sensor.dat', 'r') as file:
        data = file.readline()
    data = data.strip().split(' ')
    response = jsonify(data)
    response.status_code = 200
    print(response)
    return response

@app.route('/threshold', methods=['POST'])
def update_threshold():
    params = request.json # type: ignore
    
    print('json request: ' + str(params))

    with open('data/thresholds.pickle', 'rb') as file:
        thresholds = pickle.load(file)

    thresholds[params['threshold']] = params['value']

    with open('data/thresholds.pickle', 'wb') as file:
        pickle.dump(thresholds, file)

    res = jsonify("{}") # type: ignore    
    res.status_code = 200
    return res

@app.route('/thresholds', methods=['GET'])
def get_threshold():
    with open('data/thresholds.pickle', 'rb') as file:
        thresholds = pickle.load(file)

    return jsonify(thresholds)
    

if __name__ == '__main__':
    mqttSub.start()
    app.run(port=5000, debug=True)