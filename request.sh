#!/bin/bash

curl -X POST "http://10.2.0.188:8000/predict" \
-H "Content-Type: application/json" \
-d '{
    "Pregnancies": 1,
    "Glucose": 120,
    "BloodPressure": 70,
    "SkinThickness": 23,
    "Insulin": 94,
    "BMI": 33.6,
    "DiabetesPedigreeFunction": 0.627,
    "Age": 50
}'