from flask import render_template, jsonify, request, session, redirect, url_for, flash, send_from_directory

from app import app
import motionserver


@app.route('/execute', methods=['POST'])
def execute():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    data = request.json

    file_name_args = '/home/pi/file.m'

    points_args = ''

    for i, point in enumerate(data['points']):
        points_args += str(point[0]) + ',' + str(point[1]) + ',' + str(data['zOrT'][i]) + ','

    points_args = points_args.strip()
    points_args = points_args[:-1]

    common_args = file_name_args + ',' + points_args

    program = ''

    if data['planning'] == 'Cubic':
        program = 'path ' + str(data['T']) + ',' + str(data['k']) + ',' + common_args
    elif data['planning'] == 'Lineal Smooth':
        program = 'reference ' + common_args
    else:
        program = 'points ' + common_args

    motionserver.s.sendall(program)

    return jsonify(program=program)


@app.route('/move', methods=['POST'])
def move():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    data = request.json

    program = 'position ' + str(data['X']) + ',' + str(data['Y']) + ',' + str(data['T'])

    motionserver.s.sendall(program)

    return jsonify(program=program)


@app.route('/reset', methods=['POST'])
def reset():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    program = 'position reset'

    motionserver.s.sendall(program)

    return jsonify(program=program)


@app.route('/stop', methods=['POST'])
def stop():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    program = 'experiment stop'

    motionserver.s.sendall(program)

    return jsonify(program=program)


@app.route('/position', methods=['GET'])
def get_position():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    #motionserver.s.sendall('position ask')

    return jsonify(program='position ask')


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/image_test')
def image_test():
    #save_file = open('D:\\rpi.jpg', 'rb')
    return send_from_directory('/dev/shm/mjpeg', 'cam.jpg')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.username:
            error = 'Invalid username'
        elif request.form['password'] != app.password:
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
