from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash
import socket
import thread

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

        print 'Received:', repr(data)


DEBUG = False
SECRET_KEY = '\x1fx\x9e\xa7\x81Q\xb1\xcdZU~\x14\x0by\xff\xbeW\xf4 \xd0\xcc~\xd6\xc4'
USERNAME = 'silvio'
PASSWORD = 'silvio.1989'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/execute', methods=['POST'])
def execute():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    data = request.json

    file_name_args = 'file.m'

    points_args = ''

    for i, point in enumerate(data['points']):
        points_args += str(point[0]) + ',' + str(point[1]) + ',' + str(data['zOrT'][i]) + ','

    points_args = points_args.strip()
    points_args = points_args[:-1]

    common_args = file_name_args + ',' + points_args

    program = ''

    if data['planning'] == 'Cubic':
        program = 'path ' + str(data['T']) + ' ' + str(data['k']) + ' ' + common_args
    elif data['planning'] == 'Lineal Smooth':
        program = 'reference ' + common_args
    else:
        program = 'points ' + common_args

    s.sendall(program)

    return jsonify(program=program)


@app.route('/move', methods=['POST'])
def move():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    data = request.json

    program = 'position ' + str(data['X']) + ',' + str(data['Y']) + ',' + str(data['T'])

    s.sendall(program)

    return jsonify(program=program)


@app.route('/reset', methods=['POST'])
def reset():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    program = 'position reset'

    s.sendall(program)

    return jsonify(program=program)

@app.route('/stop', methods=['POST'])
def stop():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    program = 'experiment stop'

    s.sendall(program)

    return jsonify(program=program)


@app.route('/position', methods=['GET'])
def get_position():
    global position_flag

    program = ''

    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if not position_flag:
        program = 'position ask'
        s.sendall(program)

        while not position_flag:
            pass

        position_flag = False

    position = dict()

    position['x'] = globalPositionX
    position['y'] = globalPositionY
    position['z'] = globalPositionZ

    return jsonify(program=program, position=position)


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/boo')
def boo():
    s.sendall('position ask')
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


if __name__ == '__main__':
    HOST = '10.0.0.15'
    PORT = 50007
    s.connect((HOST, PORT))
    thread.start_new_thread(read_thread, ())
    app.run(host='0.0.0.0')
