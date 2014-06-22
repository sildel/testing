from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from app import my_app
import thread
import motionserver

if __name__ == '__main__':
    HOST = '10.0.0.15'
    PORT = 50007
    motionserver.s.connect((HOST, PORT))
    thread.start_new_thread(motionserver.read_thread, ())
    http_server = WSGIServer(('', 5000), my_app, handler_class=WebSocketHandler)
    http_server.serve_forever()