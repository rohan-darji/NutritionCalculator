from fastapi import HTTPException
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()


def get_gemini_response(input_prompt, image_data):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([input_prompt, image_data[0]])
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

def input_image_setup(uploaded_file):
    try:
        bytes_data = uploaded_file.file.read()
        image_parts = [
            {
                "mime_type": uploaded_file.content_type,
                "data": bytes_data
            }
        ]
        return image_parts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))