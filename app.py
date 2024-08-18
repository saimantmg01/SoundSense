
from flask import Flask, render_template, request, jsonify, Response
from voiceprocessor import readTxt
import time
import threading
import speech_recognition as sr
import google.generativeai as genai
import requests
import os

app = Flask(__name__)

genai.configure(api_key="AIzaSyB1zC2krSaEI-N8gLCnF0TuOUsIwFCxzWE")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 100,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def fetch_gemini_response(temp):
    try:
        response = model.generate_content([temp])
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "An error occurred: No valid response from Gemini."
    except Exception as e:
        return f"An error occurred: {str(e)}"

voice_recording = False
rec_txt = ''
temp = ''
streamer = []
loop_thread = None

def rec_loop():
    global voice_recording, rec_txt, streamer
    while voice_recording:
        for _ in range(10):
            if not voice_recording:
                break
            time.sleep(0.1)
        val = readTxt(voice_recording)
        if isinstance(val, str):
            rec_txt += val + '\n'
            streamer.append(val)
    return rec_txt

@app.route('/')
def index():
    return render_template("base.html")

@app.route('/voice-start', methods=['POST'])
def voice_start():
    global voice_recording, loop_thread
    if voice_recording:
        return jsonify(success=False, transcript='Already Recording...')
    if loop_thread and loop_thread.is_alive():
        return jsonify(success=False, message="Previous Recording is being processed...")
    
    voice_recording = True
    loop_thread = threading.Thread(target=rec_loop)
    loop_thread.start()
    return jsonify(success=True, transcript='Recording in Progress...')

@app.route('/voice-end', methods=['POST'])
def voice_end():
    global voice_recording, temp, rec_txt, loop_thread
    voice_recording = False
    temp = rec_txt
    rec_txt = ''
    if loop_thread:
        loop_thread.join()
    transcript = fetch_gemini_response(temp)
    return jsonify(success=True, transcript=transcript, user_input=temp)

@app.route('/get-gemini-response', methods=['POST'])
def get_gemini_response():
    temp = request.json.get("temp")
    transcript = fetch_gemini_response(temp)
    return jsonify(success=True, transcript=transcript)

if __name__ == "__main__":
    app.run(debug=True)
