from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash

DEBUG = True
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
