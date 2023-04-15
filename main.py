from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import requests
import os
from openai_files import FitnessGenie
from ml_model import model

app = Flask(__name__)

results = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/res')
def res():    
    data = request.args.to_dict()
    # print(data)
    w = float(data['Weight'])
    h = float(data['Height'])
    data['BMI'] = str(w / (h * h / 10000))
    data['Calorie_Deficient_or_Over'] = str(float(data['calories']) - float(data['calories_burnt']) - 2000)
    pred = model.predict(data)
    fitness_plan = FitnessGenie.ai_response(json.dumps(data), str(pred))
    return render_template('res.html', results=pred, plan=fitness_plan, billing_info=FitnessGenie.billing_resp())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)