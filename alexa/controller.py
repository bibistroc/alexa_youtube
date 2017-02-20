from flask import Response, render_template
from alexa.utils.streamer import Stream
from alexa import app, sio
from flask_socketio import emit
import logging

file_handler = ''


@app.route("/stream/<video_id>.mp3")
def stream(video_id):
    video = Stream(video_id)
    return Response(response=video.get(), status=200, mimetype='audio/mpeg',
                    headers={'Access-Control-Allow-Origin': '*', 'Content-Type': 'audio/mpeg',
                             'Content-Disposition': 'inline', 'Content-Transfer-Encoding': 'binary',
                             'Content-Length': video.length})


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')


@sio.on('connect', namespace='/log')
def test_connect():
    print 'connect'
    global file_handler

    file_handler = open('logs/web.log')
    line = file_handler.read()
    emit('content', {'content': line}, namespace='/log')


@sio.on('getMore', namespace='/log')
def get_more():
    print 'get more'
    global file_handler

    line = file_handler.read()
    emit('content', {'content': line}, namespace='/log')


@sio.on('disconnect', namespace='/log')
def test_disconnect():
    global file_handler

    file_handler.close()
    print('Client disconnected')


@sio.on('message', namespace='/log')
def handle_message(message):
    print('received message: ' + message)
