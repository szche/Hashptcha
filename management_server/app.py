from flask import Flask, render_template, request, jsonify
from database import Database
from config import SUPPORTED_HASHES
from work_dispatcher import WorkDispatcher
from test_miner import Miner


app = Flask(__name__)
database = Database()
work_dispatcher = WorkDispatcher()

@app.route("/")  
def home():
    return render_template("index.html")

# Showing hashes in database
# and form to add new hash
@app.route("/hashes")  
def hashes():
    return render_template("hashes.html", hashes=database.get_all("hashes"), supported_types=SUPPORTED_HASHES)

# Showing websites connected to the service
# And their secret-public keypairs
@app.route("/websites")  
def websites():
    return render_template("websites.html")

# Displaying an iframe with cracking client
@app.route("/frame")
def frame():
    #TODO
    return render_template("iframe.html")

# Adding new hash to the cracking database
@app.route("/hash", methods=['POST'])
def verify():
    data = request.get_json()
    database.add_hash(data['hash'], data['type'])
    return jsonify("OK"), 200

@app.route("/get-task", methods=['GET'])
def get_task():
    task = work_dispatcher.select_task(database.get_all("hashes"))
    return jsonify(task), 200


"""
@app.route("/add-site")
def verify():
    #TODO
    pass

@app.route("/remove-site")
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
    #database.add_hash("202cb962ac59075b964b07152d234b70", "MD5")
    app.run(debug=True)
    # all_hashes = database.get_all("hashes")
    # print("all hashes: ", all_hashes)
    # task = work_dispatcher.select_task(all_hashes)
    # miner = Miner()
    # completed = miner.mine(task)
    # work_dispatcher.verify_task(completed)

