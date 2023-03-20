# flask minimal app:

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
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # for more info on the instance schema, please use get_model_sample.py
    # and look at the yaml found in instance_schema_uri
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
    # print("response")
    # print(" deployed_model_id:", response.deployed_model_id)
    predictions = response.predictions
    return dict(predictions[0])

results = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.to_dict()
        # print(data)
        result = predict_tabular_classification_sample(
            project="570852395329",
            endpoint_id="7833884008462155776",
            location="us-central1",
            instance_dict=data
        )
        print(result)
        sc = result['scores']
        if sc[0] > sc[1]:
            result = 'Underweight'
        else:
            result = 'Healthy' 
        
        print("Final Result: ", result)
        
        results = result
        return redirect(url_for('res')) 
    else:
        return render_template('index.html', getres = getres)

def getres(data):
    # return results if results != "" else "not working"
    result = predict_tabular_classification_sample(
            project="570852395329",
            endpoint_id="7833884008462155776",
            location="us-central1",
            instance_dict=data
        )
    sc = result['scores']
    if sc[0] > sc[1]:
        result = 'Underweight'
    else:
        result = 'Healthy' 
    return result

@app.route('/res')
def res():
    
    data = request.args.to_dict()
    print(data)
    return render_template('res.html', results=getres(data))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)