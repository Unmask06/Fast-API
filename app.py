# app.py
import base64
import json
import logging
from io import BytesIO
from pydantic import BaseModel
import json

import pandas as pd
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set up CORS middleware options
origins = ["http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins that are allowed to make requests
    allow_credentials=True,  # Indicates whether credentials are allowed
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allows all headers
)

global_access_token = None


class DataURLRequest(BaseModel):
    dataURL: str


@app.post("/receive_token")
async def receive_token(request: Request):
    global global_access_token
    data = await request.json()
    access_token = data.get("token")
    global_access_token = access_token

    # Log the received token
    logging.info(f"Received access token: {access_token}")

    return {"data": data}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/token")
async def get_token():
    print("Helo")
    return {"token": global_access_token}


def process_token(token):
    print("Helo")
    return token


@app.post("/modifiedUserInfo")
async def modify_user_info(userInfo: dict):
    userInfo["Modified Data"] = "Sucess"
    return userInfo


# @app.post("/process-excel")
# async def process_excel(data_url: str):
#     try:
#         BinaryExcelFile = decodeDataUrl_to_Binary(data_url)
#         df = pd.read_excel(BinaryExcelFile, sheet_name=None)
#         return df
#     except Exception as e:
#         return {"error": str(e)}
@app.post("/processExcel")
async def process_excel(data: DataURLRequest):
    received_data_url = data.dataURL
    try:
        BinaryExcelFile = decodeDataUrl_to_Binary(received_data_url)
        df = pd.read_excel(BinaryExcelFile)
        df_as_dict = {
            sheet_name: df[sheet_name].to_dict() for sheet_name in df
        }
        return {"received_data_url": df_as_dict}
    except Exception as e:
        return {"error": str(e)}


def decodeDataUrl_to_Binary(data_url: str):
    # Extract the Base64-encoded data from the data URL
    data_index = data_url.find(",") + 1
    base64_data = data_url[data_index:]

    binary_data = base64.b64decode(base64_data)

    binaryFile = BytesIO(binary_data)
    return binaryFile
