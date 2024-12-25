from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, send, rooms, leave_room

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

activate_room_name = ["Lounge"]
activate_room_id = ["Public"]

activate_room = [{"room_id":0, "room_name":"Lounge"}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatting')
def chatting():
    return render_template('chatting_room.html')

@app.route("/login", methods = ["POST"])
def login():
    try:
        para = request.json
    
        session["username"] = para["username"]
        session["id"] = para["id"]

        return jsonify({"status":"OK"})
    
    except:
        return jsonify({"status":"NG"})

@socketio.on("get_username")
def temp(data):
    id = data["id"]
    username = data["username"]
    join_room(id)

    global activate_room_name, activate_room_ids
    if id not in activate_room_id:
        activate_room_id.append(id)
        activate_room_name.append(username)


@socketio.on('leave')
def on_leave(data):
    #username = data['username']
    id = data['id']
    leave_room(id)
    #send(username + ' has left the room.', to=room)

@app.route("/get_username", methods = ["POST"])
def get_username():
    try:
        username = session.get("username")
        id = session.get("id")

        return jsonify({"status":"OK", "username":username, "id":id})
    
    except:
        return jsonify({"status":"NG"})

@socketio.on("submit_message")
def submit_message(data):
    room_id = data["room_id"]
    name = data["name"]
    new_message = data["new_message"]
    time = data["time"]
    to_room_name = data["to_room_name"]
    
    print("post_people:", name , "get_people:", to_room_name,  new_message, time)
    to_room_id_index = activate_room_name.index(to_room_name)
    post_room_id_index = activate_room_name.index(name)

    if activate_room_id[to_room_id_index] == "Public":
        socketio.emit("insert_new_message", {"room_id":room_id, "post_people":name, "get_people":to_room_name,"message":new_message,"time":time})
    
    else:
        print(activate_room_id[to_room_id_index])
        socketio.emit("insert_new_message", {"room_id":room_id, "post_people":name, "get_people":to_room_name,"message":new_message,"time":time}, to = activate_room_id[to_room_id_index])
        
        socketio.emit("insert_new_message", {"room_id":room_id, "post_people":name, "get_people":to_room_name,"message":new_message,"time":time}, to = activate_room_id[post_room_id_index])



@socketio.on("invite")
def invite(data):
    invite_username = data["username"]
    invite_id = data["id"]
    invited_id = data["invited_id"]

    new_room_id = len(activate_room)


    socketio.emit("invited_request", {"room_id":new_room_id, "invite_username":invite_username, "invite_id":invite_id ,"invited_id":invited_id}, to = invited_id )

@socketio.on("accept_invite")
def accept_invite(data):
    invite_id = data["invite_id"]
    invited_name = data["invited_name"]
    room_id = data["room_id"]
    activate_room.append({"room_id":room_id})
    
    socketio.emit("response_accept_invite", {"room_id":room_id, "invited_name":invited_name}, to = invite_id)

@socketio.on("reject_invite")
def accept_invite(data):
    invite_id = data["invite_id"]

    socketio.emit("response_reject_invite", to = invite_id)

# @socketio.on('client_event')
# def client_msg(msg):...

# @socketio.on('connect_event')
# def connected_msg(msg):
#     emit('server_response', {'data': msg['data']})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)