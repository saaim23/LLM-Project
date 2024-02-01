import os
import google.generativeai as genai
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# function to load gemini
model = genai.GenerativeModel('gemini_pro_vision')


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mine_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file Uploaded")


st.set_page_config(page_title='Multi Language Invoice Extractor')
st.header('Multi Language Invoice Extractor')
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader(
    "Choose An Image....", type=["jpg,", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit = st.button('Tell me About the invoice ')
input_prompt = """"
You Are An expert in understanding invoices.We will upload  
a image as invoice and you will have to answer any question
 based on the uploaded invoice image
 """

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)
