import json
import motionserver


def handle_websocket(ws):
    print 'Start ws'
    motionserver.client_ws = ws
    while True:
        message = ws.receive()
        if message is None:
            break
        else:
            message = json.loads(message)
            ws.send(json.dumps({'output': message['output']}))

    motionserver.client_ws = None
    print 'End ws'