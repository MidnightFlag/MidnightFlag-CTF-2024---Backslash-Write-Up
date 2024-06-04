from flask import Flask, render_template, request, redirect, session, url_for, make_response, jsonify
from base64 import b64decode, b64encode
import sys, os

from utils.auth import token_required, unpack_token
from utils.database import database
from utils.ecdsa import ecdsa

app = Flask(__name__)
app.secret_key = os.urandom(16) 

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('token', '', expires=0)
    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username',None)
        signature = request.form.get('signature',None)

        if not username or not signature:
            error = 'Missing parameter(s). Please try again'
            return render_template('login.html', error=error)            

        users = database.fetch_user(username)
        if not users:
            error = 'Unknown user. Please try again'
            return render_template('login.html', error=error)

        user, sig_fetch = users

        if ecdsa.verify(sig=signature, msg=username.encode()):
            resp = make_response(redirect(url_for('home')))            
            token = b64encode((f'{user}:{signature}').encode())
            resp.set_cookie('token', token.decode())
            return resp

        error = 'Invalid signature. Please try again.'
        return render_template('login.html', error=error)

    message = session.get('message',None)
    if message is not None:
        session.pop('message')
    return render_template('login.html', message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username',None)
        if not username:
            error = 'Missing parameter. Please try again.'
            return render_template('register.html', error=error)

        users = database.fetch_user(username)
        if users:
            error = 'Username already exists. Please choose a different one.'
            return render_template('register.html', error=error)

        sig = ecdsa.sign(msg=username.encode())
        database.add_user(username, sig)

        message = ['User created, token is: ', sig]
        session['message'] = message

        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/home')
@token_required
def home():
    notes = []
    token = request.cookies.get('token')

    user, sig = unpack_token(token)
    if user:
        notes = database.fetch_notes(user=user)
        notes = [x[0] for x in notes]
            
    return render_template('home.html', notes=notes)


@app.route('/add_notes', methods=["POST"])
@token_required
def add_notes():
    content = request.form.get('content', '').strip()
    if not content:
        return redirect(url_for('home'))

    token = request.cookies.get('token')
    user, sig = unpack_token(token)
    
    if user:
        user_found = database.fetch_user_by_sig(sig=sig)
        if user_found:
            database.add_note(username=user_found[0], content=content)
    
    return redirect(url_for('home'))


with app.app_context():
    database.add_user(username='admin', sig=ecdsa.sign(b'admin'))
    database.add_note(username='admin', content=os.getenv('FLAG', 'flag{FakeFlag}'))

if __name__ == '__main__':
    app.run(
        debug=False,
        threaded=False, # Sage with threads isn't working well :(
        port=5000, 
        host="0.0.0.0"
    )