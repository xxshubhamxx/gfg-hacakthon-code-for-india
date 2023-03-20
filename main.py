from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from dotenv import load_dotenv

from typing import Dict

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


app = Flask(__name__)
load_dotenv()

def predict_tabular_classification_sample(project: str, endpoint_id: str, instance_dict: Dict, location: str , api_endpoint: str):
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    instance = json_format.ParseDict(instance_dict, Value())
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    predictions = response.predictions
    return dict(predictions[0])

results = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', getres = getres)

def getres(data):
    result = predict_tabular_classification_sample(
            project = os.environ.get('PROJECT_ID'),
            endpoint_id = os.environ.get('ENDPOINT_ID'),
            location=os.environ.get('LOCATION'),
            api_endpoint = os.environ.get('API_ENDPOINT'),
            instance_dict = data
        )
    print(dict(result))
    sc = result['scores']
    r = {}
    if sc[0] > sc[1]:
        r['class'] = 'Unhealthy'
        r['score'] = result['scores'][0]
    else:
        r['class'] = 'Healthy'
        r['score'] = result['scores'][1]
    return r

@app.route('/res')
def res():    
    data = request.args.to_dict()
    print(data)
    w = float(data['Weight'])
    h = float(data['Height'])
    data['BMI'] = str(w / (h * h / 10000))
    data['Calorie_Deficient_or_Over'] = str(float(data['calories']) - float(data['calories_burnt']) - 2000)
    return render_template('res.html', results=getres(data))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)