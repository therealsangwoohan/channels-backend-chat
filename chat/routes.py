from chat import socketio
from flask_socketio import join_room, send
from flask import request

from chat.database import get_db_connection


@socketio.on("message")
def message(data):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO message (channel_id, user_id, sent_at, text) VALUES (%s, %s, %s, %s) RETURNING *;",
                           (data["channel_id"],
                            data["user_id"],
                            data["sent_at"],
                            data["text"]))
            message_id, channel_id, user_id, sent_at, text = cursor.fetchone()

    m = {"message_id": message_id,
         "user_id": user_id,
         "text": text}
    send(m, to=channel_id)


@socketio.on("connect")
def connect(auth):
    channel_id = int(request.args.get("channel_id"))
    join_room(channel_id)
    print("Joined room", channel_id)


@socketio.on("disconnect")
def disconnect():
    print("disconnect")
    pass
