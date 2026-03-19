import string
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room as sio_join_room, leave_room as sio_leave_room
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cart-companion-secret-key'

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# ---------------------------------------------------------------------------
# MongoDB Configuration
# ---------------------------------------------------------------------------
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=1000)
    client.admin.command('ping')
    db = client['products_db']
    friends_collection = db['friends']
    prod_collection = db['prod']
    clothsec_collection = db['clothsec']
    appliances_collection = db['appliances']
    rooms_collection = db['rooms']
    mongodb_available = True
    print("MongoDB connected successfully")
except Exception as e:
    mongodb_available = False
    print(f"MongoDB not available - running without database: {e}")

# ---------------------------------------------------------------------------
# Product Data (fallback when MongoDB is unavailable)
# ---------------------------------------------------------------------------
mobile_products = [
    {"name": "iPhone", "price": "1,00,000", "image": "m1.png"},
    {"name": "Samsung Galaxy A1", "price": "75,000", "image": "m2.png"},
    {"name": "Vivo V40 Series", "price": "40,000", "image": "m3.jpg"},
    {"name": "Oppo", "price": "39,999", "image": "m4.jpg"},
    {"name": "Apple", "price": "39,999", "image": "m5.jpeg"},
]

clothing_products = [
    {"name": "Casual Shirt", "price": "29.99", "image": "shirt.jpg"},
    {"name": "Blue Jeans", "price": "49.99", "image": "jeans.jpg"},
    {"name": "Summer Dress", "price": "39.99", "image": "dress.JPG"},
    {"name": "Leather Jacket", "price": "89.99", "image": "jacket.JPG"},
    {"name": "Designer Lehanga", "price": "99.99", "image": "lehanga.JPG"},
    {"name": "Traditional Churidar", "price": "79.99", "image": "lehang.JPG"},
]

furniture_products = [
    {"name": "Sofa", "price": "15,000", "image": "sofa.jpg"},
    {"name": "Dining Table", "price": "20,000", "image": "dining_table.jpg"},
    {"name": "Chair", "price": "3,000", "image": "chair.jpg"},
    {"name": "Swing", "price": "8,000", "image": "swing.jpg"},
    {"name": "Book Case", "price": "40,000", "image": "bookcase.jpeg"},
]

appliance_products = [
    {"name": "Washing Machine", "price": "30,000", "image": "washingmachine.jpg"},
    {"name": "Refrigerator", "price": "40,000", "image": "refrigerator.jpeg"},
    {"name": "Microwave Oven", "price": "10,000", "image": "microwave.jpg"},
]

# ---------------------------------------------------------------------------
# Seed MongoDB (only if collections are empty)
# ---------------------------------------------------------------------------
if mongodb_available:
    if prod_collection.count_documents({}) == 0:
        prod_collection.insert_many([dict(p) for p in mobile_products])
    if clothsec_collection.count_documents({}) == 0:
        clothsec_collection.insert_many([dict(p) for p in clothing_products])
    if appliances_collection.count_documents({}) == 0:
        appliances_collection.insert_many([dict(p) for p in appliance_products])

# ---------------------------------------------------------------------------
# In-memory fallback stores
# ---------------------------------------------------------------------------
local_friends = []
friend_id_counter = 0
local_rooms = {}  # room_id -> { room_id, users: [], created_at }

# ---------------------------------------------------------------------------
# Helper: generate random room ID
# ---------------------------------------------------------------------------
def generate_room_id(length=8):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

# ---------------------------------------------------------------------------
# E-Commerce Routes (unchanged)
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clothes')
def clothes():
    return render_template('clothes.html', products=clothing_products)


@app.route('/mobiles')
def mobiles():
    return render_template('mobiles.html', products=mobile_products)


@app.route('/furniture')
def furniture_page():
    return render_template('furniture.html', products=furniture_products)


@app.route('/appliances')
def appliances_page():
    products = appliance_products
    if mongodb_available:
        db_products = list(appliances_collection.find())
        if db_products:
            products = db_products
    return render_template('appliances.html', products=products)


@app.route('/cart')
def cart():
    return render_template('wcart.html')


@app.route('/buy')
def buy():
    return render_template('buy.html')


@app.route('/payment')
def payment():
    return render_template('payment.html')


# ---------------------------------------------------------------------------
# Friend List Routes (with in-memory fallback)
# ---------------------------------------------------------------------------

@app.route('/friendlist', methods=['GET', 'POST'])
def friendlist():
    global friend_id_counter
    friends = []

    if request.method == 'POST':
        name = request.form.get('friend-name')
        number = request.form.get('friend-number')
        if name and number:
            if mongodb_available:
                friends_collection.insert_one({'name': name, 'number': number})
            else:
                friend_id_counter += 1
                local_friends.append({
                    '_id': str(friend_id_counter),
                    'name': name,
                    'number': number
                })

    if mongodb_available:
        friends = list(friends_collection.find())
    else:
        friends = local_friends

    return render_template('friendlist.html', friends=friends)


@app.route('/remove_friend/<friend_id>', methods=['POST'])
def remove_friend(friend_id):
    global local_friends
    if mongodb_available:
        friends_collection.delete_one({'_id': ObjectId(friend_id)})
    else:
        local_friends = [f for f in local_friends if str(f['_id']) != friend_id]
    return redirect(url_for('friendlist'))


# ---------------------------------------------------------------------------
# Room System Routes
# ---------------------------------------------------------------------------

@app.route('/create_room', methods=['POST'])
def create_room():
    """Create a new room and return its room_id."""
    room_id = generate_room_id()
    room_data = {
        'room_id': room_id,
        'users': [],
        'created_at': datetime.utcnow().isoformat()
    }

    if mongodb_available:
        rooms_collection.insert_one(dict(room_data))
    else:
        local_rooms[room_id] = room_data

    return jsonify({'success': True, 'room_id': room_id})


@app.route('/join_room/<room_id>', methods=['POST'])
def join_room_route(room_id):
    """Add a user to an existing room."""
    username = request.json.get('username', 'Anonymous') if request.is_json else 'Anonymous'

    if mongodb_available:
        room = rooms_collection.find_one({'room_id': room_id})
        if not room:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        rooms_collection.update_one(
            {'room_id': room_id},
            {'$addToSet': {'users': username}}
        )
    else:
        if room_id not in local_rooms:
            return jsonify({'success': False, 'error': 'Room not found'}), 404
        if username not in local_rooms[room_id]['users']:
            local_rooms[room_id]['users'].append(username)

    return jsonify({'success': True, 'room_id': room_id})


@app.route('/room/<room_id>')
def room_page(room_id):
    """Render the room page for WebRTC calls."""
    # Check if room exists
    room_exists = False
    if mongodb_available:
        room_exists = rooms_collection.find_one({'room_id': room_id}) is not None
    else:
        room_exists = room_id in local_rooms

    if not room_exists:
        # Auto-create room if accessed directly
        room_data = {
            'room_id': room_id,
            'users': [],
            'created_at': datetime.utcnow().isoformat()
        }
        if mongodb_available:
            rooms_collection.insert_one(dict(room_data))
        else:
            local_rooms[room_id] = room_data

    return render_template('room.html', room_id=room_id)


# ---------------------------------------------------------------------------
# Socket.IO Events for WebRTC Signaling
# ---------------------------------------------------------------------------

@socketio.on('join_room')
def handle_join_room(data):
    """User joins a socket.io room for signaling."""
    room_id = data.get('room_id')
    username = data.get('username', 'Anonymous')

    if not room_id:
        return

    # Join the socket.io room
    sio_join_room(room_id)

    # Add user to room store
    if mongodb_available:
        rooms_collection.update_one(
            {'room_id': room_id},
            {'$addToSet': {'users': username}}
        )
    else:
        if room_id in local_rooms and username not in local_rooms[room_id]['users']:
            local_rooms[room_id]['users'].append(username)

    # Notify others in the room that a new user joined
    emit('user_joined', {
        'username': username,
        'room_id': room_id
    }, to=room_id, include_self=False)

    print(f"[Room {room_id}] {username} joined")


@socketio.on('leave_room')
def handle_leave_room(data):
    """User leaves a socket.io room."""
    room_id = data.get('room_id')
    username = data.get('username', 'Anonymous')

    if not room_id:
        return

    sio_leave_room(room_id)

    # Remove user from room store
    if mongodb_available:
        rooms_collection.update_one(
            {'room_id': room_id},
            {'$pull': {'users': username}}
        )
    else:
        if room_id in local_rooms and username in local_rooms[room_id]['users']:
            local_rooms[room_id]['users'].remove(username)

    emit('user_left', {
        'username': username,
        'room_id': room_id
    }, to=room_id, include_self=False)

    print(f"[Room {room_id}] {username} left")


@socketio.on('signal')
def handle_signal(data):
    """Relay WebRTC signaling data (offer/answer/ICE) to other users in room."""
    room_id = data.get('room_id')
    signal_data = data.get('signal_data')
    signal_type = data.get('signal_type')  # 'offer', 'answer', or 'ice_candidate'

    if not room_id or not signal_data:
        return

    print(f"[Room {room_id}] Relaying signal: {signal_type}")

    # Relay to everyone else in the room
    emit('signal', {
        'signal_data': signal_data,
        'signal_type': signal_type,
        'room_id': room_id
    }, to=room_id, include_self=False)


@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")


@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")


# ---------------------------------------------------------------------------
# Run with SocketIO
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    socketio.run(app, debug=True, port=5002, allow_unsafe_werkzeug=True)
