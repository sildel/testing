import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
globalPositionX = 0
globalPositionY = 0
globalPositionZ = 0
position_flag = False


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

        print 'Received:', repr(server_data)

