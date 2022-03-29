from flask import Flask, render_template, request, jsonify
from database import Database
from config import SUPPORTED_HASHES
from work_dispatcher import WorkDispatcher
from test_miner import Miner

app = Flask(__name__)
database = Database()
work_dispatcher = WorkDispatcher()

# Main admin panel for displaying info
@app.route("/")  
def home():
    all_hashes = database.get_all("hashes")
    all_hashes_num = len(all_hashes)
    cracked_hashes = len([x for x in all_hashes if x[3] == 1])
    all_tasks = database.get_all("tasks")
    tasks_completed = [x for x in all_tasks if x[1] == 1]
    tasks_completed_num = len(tasks_completed)
    hash_counter_dict = {}
    for task in tasks_completed:
        hash_id = task[5]
        pass_point = int(task[6], 2)
        if hash_id not in hash_counter_dict:
            hash_counter_dict[hash_id] = pass_point
        elif hash_counter_dict[hash_id] < pass_point:
            hash_counter_dict[hash_id] = pass_point
    data = {
        "all_hashes": all_hashes,
        "all_hashes_num": all_hashes_num,
        "cracked_hashes": cracked_hashes,
        "all_tasks": all_tasks,
        "tasks_completed": tasks_completed_num,
        "all_hashes": sum(list(hash_counter_dict.values()))
    }
    return render_template("index.html", data=data)

# Showing hashes in database
# and form to add new hash
@app.route("/hashes")  
def hashes():
    hashes_display = []
    for h in database.get_all("hashes"):
        cracked = h[3]
        plaintext = h[4]
        tasks_hash_counter = max([int(x[6], 2) for x in database.find_tasks_for_hash(h[0]) if x[1] == 1], default=0)
        if cracked == 0:
            hashes_display.append([h[0], h[1], h[2], h[3], h[4], tasks_hash_counter])
        else:
            plaintext_int = int(plaintext, 2)
            plaintext_ascii = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big').decode()
            hashes_display.append( [h[0], h[1], h[2], h[3], plaintext_ascii, tasks_hash_counter] )
    return render_template("hashes.html", hashes=hashes_display, supported_types=SUPPORTED_HASHES)

# Showing websites connected to the service
# And their secret-public keypairs
@app.route("/websites")  
def websites():
    all_websites = database.get_all("websites")
    all_tasks = database.get_all("tasks")
    data = []
    for website in all_websites:
        w = {
            'website_id': website[0],
            'url': website[1],
            'secret_key': website[2],
            'public_key': website[3],
            'tasks_scheduled': 0,
            'tasks_completed': 0
        }
        data.append(w)
    for t in all_tasks:
        website_id = t[7]
        # Task not completed
        if t[1] == 0:
            to_add = (1, 0)
        # Task completed
        else:
            to_add = (1, 1)
        for website in data:
            if website['website_id'] == website_id:
                website['tasks_scheduled'] += to_add[0]
                website['tasks_completed'] += to_add[1]
    return render_template("websites.html", data=data)

# Displaying an iframe with cracking client
@app.route("/frame")
def frame():
    #TODO
    return render_template("iframe.html")

# Adding new hash to the cracking database
@app.route("/hash", methods=['POST'])
def hash():
    data = request.get_json()
    database.add_hash(data['hash'], data['type'])
    return jsonify("OK"), 200

# Returns a random task to crack
@app.route("/get-task", methods=['GET'])
def get_task():
    key = request.args.get('k')
    task = work_dispatcher.select_task(database.get_all("hashes"), key)
    return jsonify(task), 200

# Verifies the task has been completed correctly
# Collects data on work done
@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    verification = work_dispatcher.verify_task(data)
    if verification == True:
        return jsonify("Ok"), 200
    return jsonify("Error"), 403

# Adds new website to the database
@app.route("/website", methods=["POST"])
def add_new_website():
    data = request.get_json()
    return_data = database.add_new_website(data['url'])
    return jsonify(return_data), 200



if __name__ == "__main__":
    app.run(debug=True)
