import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from utils import get_gemini_response, input_image_setup
import google.generativeai as genai
import json
import re

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
app = FastAPI()

input_prompt = """ 
You are an expert nutritionist. Based on the image, calculate the total calories and provide details of every food item with its calorie intake in the following format:

**Food Items:**
1. Item 1 - Number of calories
2. Item 2 - Number of calories

**Healthiness:** 
State if the food is healthy or not.

**Nutrient Breakdown:**
Provide a percentage breakdown of carbohydrates, protein, fats, and other important nutrients in a healthy diet.
Do not include the Disclaimer. Do not  iclude the unknown nutrient info in the response.

Output the response in a structured format like this:
{
    "total_calories": Number,
    "food_items": [
        {"item": "Item 1", "calories": Number},
        {"item": "Item 2", "calories": Number}
    ],
    "healthiness": "Healthy/Unhealthy",
    "nutrient_breakdown": {
        "carbohydrates": "amount in grams or %",
        "protein": "amount in grams or %",
        "fats": "amount in grams or %",
        "fiber": "amount in grams or %",
        "sugar": "amount in grams or %",
    }
}
do not mention the response type or the response format in the response.. give the response strictly in the format mentioned above.
"""

@app.get("/")
async def root():
    return {"message": "Welcome to the Nutrition Calculator API!"}

@app.post("/calculate-nutrition/")
async def calculate_nutrition(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image uploaded.")
    
    if image.content_type not in ["image/jpg", "image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JPG, JPEG or PNG image.")
    

    image_data = input_image_setup(image)
    response = get_gemini_response(input_prompt, image_data)
    if not response:
        raise HTTPException(status_code=500, detail="Error processing the image.")
    try:
        cleaned_response = re.search(r'\{.*\}', response, re.DOTALL)

        if not cleaned_response:
            raise ValueError("No valid JSON found in the response.")

        json_str = cleaned_response.group(0)  # Extract only the JSON part

        # Convert to dictionary
        data = json.loads(json_str)  # Ensure response is JSON-formatted

        # Extract relevant details
        total_calories = data.get("total_calories", 0)
        food_items = [{"item": item["item"], "calories": item["calories"]} for item in data.get("food_items", [])]
        healthiness = data.get("healthiness", "Unknown")
        nutrient_breakdown = data.get("nutrient_breakdown", {})

        # Return the structured JSON response
        return {
            "total_calories": total_calories,
            "food_items": food_items,
            "healthiness": healthiness,
            "nutrient_breakdown": nutrient_breakdown
        }


    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse response from the model.")
    