from flask import Flask, request
from dotenv import load_dotenv
import os
import openai
from datetime import datetime

load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

def ai_response(data, pred):
    prompt = "Suggest a workout plan for me. My health details are: " + data + " Please note that height is in cm and weight is present in kg. I also created a machine learning model trained using Google's AutoML to predict whether I am healthy or not. Here are the results: " + pred + " Don't rely on model's output as it has only about 90% accuracy. Suggest a detailed workout plan for me."
    print("ChatGPT Prompt: ", prompt)
    response = openai.Completion.create(
        engine = 'text-davinci-003',
        prompt = prompt,
        temperature = 0.75,
        max_tokens = 100
    )
    print("ChatGPT Response: ", response)
    refine_response = str(response['choices'][0]['text'])
    paragraphs = refine_response.split('\n\n')
    html_response = ''
    for p in paragraphs:
        html_response += f'<p>{p}</p>'
    
    today = datetime.today().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bal = openai.api_requestor.APIRequestor().request("get", "/usage",{"date": today}, {"time": time}, {"timestamp": timestamp})
    resp = bal[0].data['data']
    print("Billing Usage Respose: ",resp)
    total_usage = sum([item['n_generated_tokens_total'] for item in resp])
    remaining_tokens = 900000 - total_usage
    print(f"Remaining credits: {remaining_tokens}")
    
    html_response += f"<br><br> <p>Remaining tokens: {remaining_tokens} (approx ${remaining_tokens*0.02/1000} out of $18 ) </p>"
    
    return html_response