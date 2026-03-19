# 🛒 Cart Companion

Cart Companion is a **real-time collaborative shopping platform** that enables users to shop together just like in a physical store. Users can create or join rooms, communicate using audio/video or screen sharing, and explore products together in real time.

---

## 🚀 Features

### 🧑‍🤝‍🧑 Collaborative Shopping

* Create or join shopping rooms instantly
* Invite friends and shop together
* Shared browsing experience in real time

### 📡 Real-Time Communication

* Peer-to-peer audio/video using WebRTC
* Screen sharing support
* Low-latency interaction

### ⚡ Real-Time Signaling

* Built using Flask-SocketIO
* Handles WebRTC offer/answer exchange
* ICE candidate relay system

### 🛍️ E-commerce Functionality

* Browse products by categories:

  * Clothes
  * Mobiles
  * Furniture
  * Appliances
* Add to cart
* Basic checkout flow

### 👥 Friend System

* Add and manage friends
* Start shopping sessions directly with friends

---

## 🏗️ Tech Stack

### Backend

* Flask (Python)
* Flask-SocketIO (real-time communication)
* MongoDB (data storage)

### Frontend

* HTML, CSS, JavaScript
* WebRTC (peer-to-peer media streaming)

---

## 🧠 How It Works

### 🔹 Room System

* Users create or join a room
* Room data is stored in MongoDB
* Multiple users can join the same session

### 🔹 Signaling (Server Role)

WebRTC requires signaling to establish connections.

Flask-SocketIO is used to:

* Send offer
* Send answer
* Exchange ICE candidates

⚠️ The server does NOT handle media streams.

### 🔹 Media Flow (WebRTC)

* Once connected:

  * Audio/video/screen streams flow peer-to-peer
  * No server bandwidth is used for media

---

## 🔄 Workflow

1. User creates a room
2. Another user joins using Room ID
3. WebRTC connection is established:

   * Offer → Server → Peer
   * Answer → Server → Peer
   * ICE candidates exchanged
4. Direct peer-to-peer connection is formed
5. Users can:

   * Talk
   * Share screen
   * Shop together

---

## 📂 Project Structure

```
project/
│── app.py
│── templates/
│   ├── base.html
│   ├── index.html
│   ├── room.html
│   ├── friendlist.html
│   └── ...
│── static/
│   ├── css/
│   ├── js/
│   └── images/
```

---

## ▶️ Getting Started

### 1. Clone the repository

```
git clone <your-repo-link>
cd cart-companion
```

### 2. Install dependencies

```
pip install flask flask-socketio pymongo
```

### 3. Run the app

```
python app.py
```

### 4. Open in browser

```
http://127.0.0.1:5002
```

---

## 🧪 Testing Real-Time Feature

1. Open the app in **two browser tabs**
2. Create a room in one tab
3. Join the same room in another tab
4. Start call or screen share

---

## 🎯 Key Highlights

* Real-time collaboration using WebRTC
* Efficient signaling using Flask-SocketIO
* Peer-to-peer architecture (no media load on server)
* Clean, modern, production-style UI

---

## 🔮 Future Improvements

* Real-time shared cart synchronization
* Authentication system
* Group calls (multi-user support)
* Chat integration
* TURN server for production deployment

---

## 👩‍💻 Author

**Nida Masarrath**

---

## ⭐ License

This project is for educational and demonstration purposes.
