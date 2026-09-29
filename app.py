import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from extract_url_features import extract_url_features
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
FRONTEND_URL = os.getenv("FRONTEND_URL")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

model = joblib.load("Final_Phishing_Model.pkl")

@app.post("/predict")
def Predict_Url(data: URLRequest):

    try:
        url = data.url.strip()

        if not url:
            return {
                "error": "URL is required"
            }

        features = extract_url_features(url)

        print("\nExtracted Features:")
        print(features)

        X_new = pd.DataFrame([
      {
            "URL": url,
            **features
      }
      ])

        print("\nX_new:")
        print(X_new)

        print("\nShape:", X_new.shape)

        prediction = int(
            model.predict(X_new)[0]
        )

        probability = model.predict_proba(X_new)[0]

        phishing_probability = float(probability[0]) * 100
        legitimate_probability = float(probability[1]) * 100

        result = (
            "legitimate"
            if prediction == 1
            else "phishing"
        )

        response = {
            "url": url,
            "prediction": prediction,
            "result": result,
            "legitimate_probability": round(
                legitimate_probability,
                2
            ),
            "phishing_probability": round(
                phishing_probability,
                2
            )
        }
        return response

    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__
        }