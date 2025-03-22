import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel("gemini-2.0-flash")
    reponse = model.generate_content([input_prompt, image[0]])
    return reponse.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return FileNotFoundError("No file uploaded")
    

#Streamlit app
st.set_page_config(page_title="Nutrition Calculator")

st.header("Calories Calculator")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

submit_button = st.button("Calulate Nutrition")


input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image and calculate the total calories, also provide the details of every food items with calories intake is below format

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----
Finally you can also mention if the food is healthy or not and also mention the percentage split of the ratio of cabohydrates, protein, sugar, fats and other important nutrients required in our diet. Do not include the Disclaimer. Just repond to the user's query and provide the details of the food items with calories intake in the above format.
"""

if submit_button:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.header("Calculated Calories")
    st.write(response)