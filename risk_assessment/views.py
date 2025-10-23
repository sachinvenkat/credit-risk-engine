from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR =  Path(__file__).resolve().parent
MODEL_PATH =  BASE_DIR / 'model' / 'risk_model.pkl'

try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    print(f"Error:Model not found at {MODEL_PATH} ")
    model = none
except Exception as e:
    print(f"Error loading model:{e}")
    model = none

def create_dummy_dataframe(form_data):
    all_columns = [
        'checking_account_status', 'duration', 'credit_history', 'purpose', 'credit_amount',
        'savings_account', 'employment_status', 'installment_rate', 'personal_status_sex',
        'other_debtors', 'present_residence', 'property', 'age', 'other_installment_plans',
        'housing', 'number_of_existing_credits', 'job', 'dependents', 'telephone', 'foreign_worker'
    ]
    default_values = {
        'checking_account_status': 'A14', 'duration': 24, 'credit_history': 'A32', 'purpose': 'A40',
        'credit_amount': 2500, 'savings_account': 'A61', 'employment_status': 'A73',
        'installment_rate': 4, 'personal_status_sex': 'A93', 'other_debtors': 'A101',
        'present_residence': 4, 'property': 'A121', 'age': 35, 'other_installment_plans': 'A143',
        'housing': 'A152', 'number_of_existing_credits': 1, 'job': 'A173', 'dependents': 1,
        'telephone': 'A191', 'foreign_worker': 'A201'
    }
    df = pd.DataFrame(default_values, index=[0])

    for key, value in form_data.items():
        if key in df.columns:
            try:
                df[key] = pd.to_numeric(value)
            except ValueError :
                df[key] = value
    return df
# views

def home(request):
    return render(request, 'risk_assessment/index.html')

def predict(request):
    prediction_text=""
    probability_text=""

    if request.method == 'POST' and model:
        try:
            form_data = request.POST.copy()
            form_data.pop('csrfmiddlewaretoken', None)

            live_data = create_dummy_dataframe(form_data)

            prediction = model.predict(live_data)[0]

            probability = model.predict_proba(live_data)[0][1]

            if prediction == 1:
                prediction_text = "Approved (Good Risk)"
            else:
                prediction_text = "Declined (Bad risk)"

            probability_text =  f"{probability * 100:.2f}%" 

        except Exception as e:
            print(f"Prediction Error: {e}")
            prediction_text = f"Error making prediction: {e}"

    context = {
        'prediction_text' : prediction_text,
        'probability_text' : probability_text
    }
    return render(request, 'risk_assessment/index.html', context)






