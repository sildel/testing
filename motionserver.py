import json
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
globalPositionX = 0
globalPositionY = 0
globalPositionZ = 0
position_flag = False
client_ws = None


def read_thread():
    global globalPositionX, globalPositionY, globalPositionZ, position_flag
    while 1:
        server_data = s.recv(1024)
        command, data = server_data.split(' ')
        if command == 'position':
            coordinates = data.split(',')
            globalPositionX = float(coordinates[0])
            globalPositionY = float(coordinates[1])
            globalPositionZ = float(coordinates[2])
            position_flag = True
            if client_ws is not None:
                try:
                    client_ws.send(json.dumps({'position': [globalPositionX, globalPositionY, globalPositionZ]}))
                except Exception:
                    print Exception.message




        # print 'Received:', repr(server_data)

