from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)

from typing import Dict

from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


def predict_tabular_classification_sample(
    project: str,
    endpoint_id: str,
    instance_dict: Dict,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
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
            project="570852395329",
            endpoint_id="7833884008462155776",
            location="us-central1",
            instance_dict=data
        )
    sc = result['scores']
    if sc[0] > sc[1]:
        result = 'Unhealthy'
    else:
        result = 'Healthy' 
    return result

@app.route('/res')
def res():
    
    data = request.args.to_dict()
    print(data)
    data['BMI'] = str((int(data['Weight']) * 10000 / (int(data['Height']) * int(data['Height']))))
    data['Calorie_Deficient_or_Over'] = str(int(data['calories']) - int(data['calories_burnt']) - 2000)
    return render_template('res.html', results=getres(data))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)