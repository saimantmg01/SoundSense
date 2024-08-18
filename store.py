#render template allows you to run html and js
from flask import Flask, render_template, request, jsonify, Response
from voiceprocessor import readTxt
import time
import threading
import speech_recognition as sr
#reference this file
app = Flask(__name__)


# Define your Python function to set the variable to True
voice_recording = False
rec_txt = ''
temp = ''
streamer = []
loop_thread = None
# Define your Python function to set the variable to True
def rec_loop():
    global voice_recording, rec_txt, streamer
    while voice_recording:
        print(voice_recording)
        for _ in range(10):
            if not voice_recording:
                break
            time.sleep(0.1)
        val = readTxt()
        if(type(val) == str):
            rec_txt += val + '\n'
            streamer.append(val)
        
    return rec_txt

#routes
@app.route('/') #decorators for route handling
def index():
    # return "Hello, World!"
    return render_template("index.html")

# Define a route to handle the button click (without page refresh)
@app.route('/voice-start', methods=['POST'])
def voice_start():
    global voice_recording 
    global loop_thread
    if(voice_recording):
        return jsonify(success=False, transcript='Already Recording...')
    if loop_thread and loop_thread.is_alive():
        return jsonify(success=False, message="Previous Recording is being processed...")
    voice_recording= True
    loop_thread = threading.Thread(target=rec_loop)
    loop_thread.start()
    return jsonify(success=True, transcript='Recording in Progress...')  # Return a JSON response


@app.route('/voice-end', methods=['POST'])
def voice_end():
    global voice_recording
    voice_recording = False
    global temp
    global rec_txt
    global loop_thread
    temp = rec_txt
    rec_txt = ''
    print("end", temp)
    if loop_thread:
        loop_thread.join()  # Wait for the thread to finish
    return jsonify(success=True, transcript=temp)  # Return a JSON response

@app.route('/stream')
def stream():
    def event_stream():
        while voice_recording or len(streamer) > 0 :
            if len(rec_txt) > 0:
                yield f"data: {streamer.pop(0)}\n\n"
            time.sleep(0.1)
    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    #debug will show errors on webpage
    app.run(debug=True)

