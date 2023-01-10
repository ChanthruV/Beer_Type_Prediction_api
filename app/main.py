from fastapi import FastAPI
from starlette.responses import JSONResponse
from joblib import load
import pandas as pd
#from pydantic import BaseModel

app = FastAPI()

nn_pipe = load("../models/neural_network")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/health', status_code=200)
def healthcheck():
    return 'Neural Network is all ready to go!'

##class BeerType(BaseModel): 
    #brewery_name: float
    #review_aroma: float
    #review_appearance: float
    #review_palate: float
    #review_taste: float

#def format_features(review_aroma: float, review_appearance: float, review_palate: float, review_taste: float):
    #return {
        #'review_aroma (0-5)': [review_aroma],
        #'review_appearance (0-5)': [review_appearance],
        #'review_palate (0-5)': [review_palate],
        #'review_taste (0-5)': [review_taste]
    #}

#@app.post("/beer/type/")
#def predict(item: BeerType):
   # return item
