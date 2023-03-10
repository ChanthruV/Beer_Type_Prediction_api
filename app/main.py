from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from starlette.responses import JSONResponse
import torch
import pandas as pd
import numpy as np
from joblib import load

import sys
sys.path.insert(1, '..')
from pytorch import PytorchMultiClass
model=PytorchMultiClass(num_features=12)
model.load_state_dict(torch.load("../models/neural_network.pt"))

app = FastAPI()
nnsc=load("../models/scaler_dropped_NN.joblib")


@app.get("/")
def read_root():
    return {"Description of project objectives": "To build a NN that can accurately predict beer type given user ratings. To deploy it via a web app with Heroku",
            "List of endpoints":"'/', '/health/', '/beer/type/', 'beers/type', '/model/architecture/'",
            "Input parameters":"brewery_name:str, review_aroma:float, review_appearance:float, review_palate:float, review_taste:float",
            "Output Layers":"layer1=12, layer2=32",
            "Link to Github repo":"https://github.com/ChanthruV/Beer_Type_Prediction_api.git"
            }
    


@app.get('/health/', status_code=200)
def healthcheck():
    return "Status code is 200. Neural Network model is ready to predict!"



class Item(BaseModel):
    brewery_name: str
    review_aroma: float
    review_appearance: float
    review_palate: float
    review_taste: float

def format_features(item: Item):
    return {
        'brewery_name': [item.brewery_name],
        'review_aroma': [item.review_aroma],
        'review_appearance': [item.review_appearance],
        'review_palate': [item.review_palate],
        'review_taste': [item.review_taste]
    }



@app.post("/beer/type/")
def predict(item:Item):
    features = format_features(item)
    df=pd.DataFrame.from_dict(features)
    df.drop('brewery_name',axis=1,inplace=True)
    num_cols=['review_aroma','review_appearance','review_palate','review_taste']
    df[num_cols]=nnsc.transform(df[num_cols])
    obs = torch.Tensor(df.to_numpy())
    pred_index= model(obs)[0].argmax(0)
    pred= ([np.array(pred_index)])
    return JSONResponse(pred.tolist())    

class Item_multi(BaseModel):
    brewery_name: List[str]
    review_aroma: List[float]
    review_appearance: List[float]
    review_palate: List[float]
    review_taste: List[float]


def format_features_multi(items:Item_multi):
    return {
        'brewery_name': items.brewery_name,
        'review_aroma': items.review_aroma,
        'review_appearance': items.review_appearance,
        'review_palate': items.review_palate,
        'review_taste': items.review_taste
    }


@app.post("/beers/type/")
def predict(items:Item_multi):
    features = format_features_multi(items)
    df=pd.DataFrame.from_dict(features)
    df.drop('brewery_name',axis=1,inplace=True)
    num_cols=['review_aroma','review_appearance','review_palate','review_taste']
    df[num_cols]=nnsc.transform(df[num_cols])
    pred=[]
    for i in range(0,df.shape[0]):
        obs = torch.Tensor(df.iloc[[i]].to_numpy())
        y_index= model(obs)[0].argmax(0)   
        y= ([np.array(y_index)])[0] 
        pred.append(y)   
    return JSONResponse(pred)

@app.get("/model/architecture/")
def model_arch():
    return model