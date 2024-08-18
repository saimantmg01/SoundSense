
"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""
import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3 
import time
import requests
from flask import Response

genai.configure(api_key="AIzaSyB1zC2krSaEI-N8gLCnF0TuOUsIwFCxzWE")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 100, #limit the output content
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)
#function to get input 
# def get_promt():
#     return tester1()

chat_session = model.start_chat(
  history=[] #to create a new chat with no history 
)

prompt = input("Prompt: ")
print(f"responding for: {prompt}")


# response = chat_session.send_message(prompt)
try:
    response = chat_session.send_message(prompt)
    print(response.text)
except Exception as e:
    print(f"Line 48 llm- An error occurred: {e}")

