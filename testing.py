from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash
import os

DEBUG = False
SECRET_KEY = '\x1fx\x9e\xa7\x81Q\xb1\xcdZU~\x14\x0by\xff\xbeW\xf4 \xd0\xcc~\xd6\xc4'
USERNAME = 'silvio'
PASSWORD = 'silvio.1989'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/am-i-the-best')
def question():
    return 'Yes, you are!'


@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@app.route('/my_add', methods=['POST'])
def add_numbers_post():
    a = request.form.get('a', 0, type=int)
    b = request.form.get('b', 0, type=int)

    return jsonify(result=a - b)


@app.route('/execute', methods=['POST'])
def execute():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    data = request.json

    file_name_args = 'temp.m'

    points_args = ''

    for i, x in enumerate(data['xArray']):
        points_args += str(x) + ' ' + str(data['yArray'][i]) + ' ' + str(data['zOrT'][i]) + ' '

    points_args = points_args.strip()

    common_args = file_name_args + ' ' + points_args

    program = ''

    if data['planning'] == 'path':
        program = 'sudo /home/pi/path/path ' + str(data['T']) + ' ' + str(data['k']) + ' ' + common_args
    elif data['planning'] == 'points':
        program = 'sudo /home/pi/points/points ' + common_args
    else:
        program = 'sudo /home/pi/reference/reference ' + common_args

    os.system(program)

    file = open('temp.m')
    string = file.read()
    file.close()

    return jsonify(program=program, string=string)


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')


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
    app.run(host='0.0.0.0')
