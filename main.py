from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from api.end_points.search_to_provider import generate_gpt_response
import google.generativeai as genai
import os
from fastapi.encoders import jsonable_encoder

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class InputMessage(BaseModel):
    input_mes: str
    in_provider: str
class OutputResult(BaseModel):
    response: str

origins = [
    "http://localhost",           # Add the URL of your frontend application
    "http://localhost:3000",      # Add the URL of your frontend application with the specific port
    # Add more origins as needed
]
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
# TODO: controller
@app.post("/generate-keywords", response_model=OutputResult)
def generate_keywords(input_api: InputMessage):
    try:
        result = generate_gpt_response(input_api.in_provider, input_api.input_mes)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("API Documentation","http://127.0.0.1:6080/docs")
    uvicorn.run(app, host="127.0.0.1", port=6080)
