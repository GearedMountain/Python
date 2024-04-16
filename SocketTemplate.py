from flask import Flask, render_template, request, session, redirect,url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import math
import time
app = Flask(__name__, static_folder='static')
app.config["SECRET_KEY"] = "ShadowTheFeline"
socketio = SocketIO(app)
rooms = {}

#Generate random 4 letter all uppercase code and 
#ensure its not being used already
def generateCode(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break       
    return code

@app.route("/", methods=["POST","GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")   
        join = request.form.get("join", False)   
        create = request.form.get("create", False)
        if not name:
            return render_template("home.html",error="Please enter a name", code=code,name=name)
        if join != False and not code:
            return render_template("home.html",error="Please enter a code", code=code,name=name)
        room = code
        if create != False:
            room = generateCode(4)
            rooms[room] = {"members":0,"messages":[]}
        elif code not in rooms:
            return render_template("home.html",error="Room does not exist", code=code,name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("game"))
    return render_template("home.html")




@app.route("/game")
def game():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("game.html",code=room)

#@socketio.on("message") waits for message to arrive then handles it
@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    send({"header": data["header"],"information":data["data"]},to=room,include_self=False)

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
        
    join_room(room)
    send({"name": name,"points":0},to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    
    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    print(f"{name} left room {room}")   
    
if __name__ == "__main__":
#host=""
#provides the private ip address of your computer, this will be
#the ip address required to access the website
    socketio.run(app,host="127.0.0.1",debug=True)