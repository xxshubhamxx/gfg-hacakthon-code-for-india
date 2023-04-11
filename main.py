from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import requests
import os
from openai_files import FitnessGenie

app = Flask(__name__)

results = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', getres = getres)

def getres(data1):
    print("Input data:",data1)
    data = {
        "instances": [
            {
                "step_count": data1['step_count'],
                "calories_burnt": data1['calories_burnt'],
                "hours_of_sleep": data1['hours_of_sleep'],
                "Weight": data1['Weight'],
                "Height": data1['Height'],
                "calories": data1['calories'],
                "BMI": data1['BMI']
            }
        ]
    }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post('https://gcp-model-service-emffglsbhq-uc.a.run.app/predict', data=json.dumps(data), headers=headers)
    prediction = response.json()
    tempresult = jsonify(prediction)
    result = tempresult.get_json()['predictions'][0]
    print("AutoML Model Output: ",result)
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
    # print(data)
    w = float(data['Weight'])
    h = float(data['Height'])
    data['BMI'] = str(w / (h * h / 10000))
    data['Calorie_Deficient_or_Over'] = str(float(data['calories']) - float(data['calories_burnt']) - 2000)
    pred = getres(data)
    return render_template('res.html', results=pred, plan=FitnessGenie.ai_response(json.dumps(data), str(pred)))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)