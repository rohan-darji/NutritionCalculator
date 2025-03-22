import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from utils import get_gemini_response, input_image_setup
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
app = FastAPI()

input_prompt = """ 
You are an expert in nutritionist where you need to see the food items from the image and calculate the total calories, also provide the details of every food items with calories intake is below format

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----
Finally you can also mention if the food is healthy or not and also mention the percentage split of the ratio of cabohydrates, protein, sugar, fats and other important nutrients required in our diet. Do not include the Disclaimer. Just repond to the user's query and provide the details of the food items with calories intake in the above format.
"""

@app.get("/")
async def root():
    return {"message": "Welcome to the Nutrition Calculator API!"}

@app.post("/calculate-nutrition")
async def calculate_nutrition(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image uploaded.")
    
    if image.content_type not in ["image/jpg", "image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JPG, JPEG or PNG image.")
    

    image_data = input_image_setup(image)
    reponse = get_gemini_response(input_prompt, image_data)
    if not reponse:
        raise HTTPException(status_code=500, detail="Error processing the image.")
    return {"Calculated Nutrition": reponse}
    