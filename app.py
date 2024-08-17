#render template allows you to run html and js
from flask import Flask, render_template


#reference this file
app = Flask(__name__)



#routes
@app.route('/') #decorators for route handling
def index():
    # return "Hello, World!"
    return render_template("index.html")

if __name__ == "__main__":
    #debug will show errors on webpage
    app.run(debug=True)

