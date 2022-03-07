from flask import Flask, render_template
from database import Database

app = Flask(__name__)
database = Database()


@app.route("/")  
def home():
    return render_template("index.html")

@app.route("/frame")
def frame():
    #TODO
    return render_template("iframe.html")
"""
@app.route("/add-site")
def verify():
    #TODO
    pass

@app.route("/remove-site")
def verify():
    #TODO
    pass

@app.route("/submit-hash")
def verify():
    #TODO
    pass


@app.route("/get-task")
def get_task():
    #TODO
    pass

@app.route("/verify")
def verify():
    #TODO
    pass

"""

if __name__ == "__main__":
    
    app.run(debug=True)

