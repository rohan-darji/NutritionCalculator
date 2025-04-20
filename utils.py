from fastapi import HTTPException
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()


def get_gemini_response(input_prompt, image_data):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

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