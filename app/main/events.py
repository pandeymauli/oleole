from flask import session
from flask_socketio import emit, join_room, leave_room
import re
#import emoji
from emoji import emojize
from .. import socketio

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    text = emojize(message['msg'] , use_aliases=True)
    print(text)
    # regExp = r':(.+?):'
    # text = str(message['msg'])
    # print(type(text), text, type(str(text)), str(text))
    # emojisInMessage = re.findall(regExp, text)
    # if(emojisInMessage):
    #     print("Emojis found in message... ", emojisInMessage)
    #     for emoji in emojisInMessage:
    #         emoji = ':'+emoji+':'
    #         print(emojize(emoji, use_aliases = True))
    #         emojiConverted = emojize(emoji, use_aliases = True)
    #         text = text.replace(emoji , emojiConverted)
    emit('message', {'msg': session.get('name') + ':' + text}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
