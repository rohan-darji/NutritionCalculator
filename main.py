import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils import fetch_user_allergies, get_gemini_response, input_image_setup
import google.generativeai as genai
import json
import re

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


input_prompt = """
You are an expert nutritionist. Based on the image, calculate the total calories and provide details of every food item with its calorie intake in the following format:

**Food Items:**
1. Item 1 - Number of calories
2. Item 2 - Number of calories

**Healthiness:** 
State if the food is healthy or not.

**Nutrient Breakdown:**
Provide a percentage breakdown of carbohydrates, protein, fats, and other important nutrients in a healthy diet.
Do not include the Disclaimer. Do not include the unknown nutrient info in the response.

In addition, consider the user's allergy profile below and evaluate whether the food is safe for them to consume. Use the severity to guide your decision:

**Allergy Profile:**
- Substance 1 (severity: mild/moderate/severe)
- Substance 2 (severity: ...)

Clearly assess if any of the food items contain or may contain these substances. If so, explain the risk and set the `safe_to_eat` field accordingly.

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
        "sugar": "amount in grams or %"
    },
    "is_safe_to_consume": true/false
}
Do not include any other explanation or response format details. Return strictly the structured JSON above.
"""


@app.get("/")
async def root():
    return {"message": "Welcome to the Nutrition Calculator API!"}

@app.post("/calculate-nutrition/")
async def calculate_nutrition(user_id: str = Form(...), image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image uploaded.")
    
    if image.content_type not in ["image/jpg", "image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a JPG, JPEG or PNG image.")
    
    allergy_data = fetch_user_allergies(user_id)
    allergy_context = "\n".join([
        f"- {item['substance']} ({item['severity']})"
        for item in allergy_data
    ]) or "None"
    

    image_data = input_image_setup(image)
    full_prompt = input_prompt.replace(
    "**Allergy Profile:**\n- Substance 1 (severity: mild/moderate/severe)",  # placeholder
    f"**Allergy Profile:**\n{allergy_context or '- None'}"  # dynamic data
    )

    response = get_gemini_response(full_prompt, image_data)
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
        is_safe_to_consume = data.get("is_safe_to_consume", None) 

        # Return the structured JSON response
        return {
            "total_calories": total_calories,
            "food_items": food_items,
            "healthiness": healthiness,
            "nutrient_breakdown": nutrient_breakdown,
            "is_safe_to_consume": is_safe_to_consume
        }


    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse response from the model.")
    