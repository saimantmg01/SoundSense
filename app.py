#render template allows you to run html and js
from flask import Flask, render_template, request, jsonify
from voiceprocessor import tester1

#reference this file
app = Flask(__name__)


# Define your Python function to set the variable to True
voice_start = False

# Define your Python function to set the variable to True
def set_voice_start_true():
    global voice_start
    voice_start = True
def set_voice_start_false():
    global voice_start
    voice_start = False

#routes
@app.route('/') #decorators for route handling
def index():
    # return "Hello, World!"
    return render_template("index.html")

# Define a route to handle the button click (without page refresh)
@app.route('/voice-start', methods=['POST'])
def voice_start_route():
    set_voice_start_true()
    transcript = tester1()
    set_voice_start_false()
    return jsonify(success=True, transcript=transcript)  # Return a JSON response

# @app.route('/voice-end', methods=['POST'])
# def voice_start_route():
#     set_voice_start_false()
#     transciprt = tester1()
#     return jsonify(success=True, transciprt=transciprt)  # Return a JSON response


if __name__ == "__main__":
    #debug will show errors on webpage
    app.run(debug=True)

