from chat import socketio, app

if __name__ == '__main__':
    socketio.run(app, host="localhost", port=4500, debug=True)
