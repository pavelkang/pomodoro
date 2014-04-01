# oauth_verifier is different every time E15F1E72E60D985F48AD6BFCF46D1F5E
# oauth_token is different
from flask import *
from functools import wraps
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from auth import *
import estimate, execute

import facebook
import fbBasicOps as fbOP
import fbAuth

app = Flask(__name__)
app.secret_key = 'admin'
(goto_auth_url, request_token) = get_goto_url()

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to log in.")
            return redirect(url_for('log'))
    return wrap

@app.route('/') # main URL
def home():
    return render_template('home.html')

@app.route('/laopo') # main URL
def laopo():
    return render_template('laopo.html')

@app.route('/App') # App URL
def App():
    messages = ['112hw', '122lab']
    # return render_template('App.html', messages=messages, messages_range=range(len(messages)))
    if "oauth_verifier" in request.url:
        authurl = request.url
        auth_token = get_auth_token(request_token, authurl)
        authorize_data = authorize(auth_token)
        session["auth_token"] = authorize_data[1]
        messages = authorize_data[0]
    else:
        return render_template('App.html')
    return render_template('App.html', messages=messages, messages_range=range(len(messages)))

@app.route('/hello') # hello URL
@login_required
def hello():
    return render_template('hello.html')

@app.route('/signup') # sign-up URL
def signup():
    return render_template('signup.html')

@app.route('/App1') # App1 URL
def App1():
    return render_template('App1.html')

@app.route('/giveup') # App1 URL
def giveup():
    return render_template('giveup.html')

@app.route('/finish') # App1 URL
def finish():
    fb_url = fbAuth.get_goto_url()
    auth_url = ""
    if "?code=" in request.url:
        auth_url = request.url
        RAWauthtoken = fbAuth.get_auth_token(request.url)
        authtoken = RAWauthtoken['access_token']
        fbOP.postFacebook(authtoken,"I have finished a task on Pomodoro! It is fun!")
    return render_template('finish.html', fb_url=fb_url, auth_url=auth_url)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('log'))

@app.route('/auth') # auth URL
def auth():
    url = None
    return render_template('auth.html', url=goto_auth_url)

@app.route('/love')
def love():
    return "I miss you so much/n"

@app.route('/log', methods=['GET','POST'])
def log():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = "sorry. please try again."
        else:
            session["logged_in"] = True
            return redirect(url_for('hello'))
    return render_template('log.html', error=error)

@app.route('/cobot', methods=['GET', 'POST']) # cobot URL
def cobot():
    # return "40,40"
    error = None
    info = None
    if request.method == 'POST':
        if request.form['username'].startswith("cobot"):
            print "HANDLIING POST REQUEST FROM PHONE"
            info = request.form['username'][5:]
            return estimate.main(info)
        if request.form['username'].startswith("sendCobot"):
            print "Sending signal to Cobot ..."
            info = request.form['username'][9:]
            return execute.main(info)
    return render_template('cobot.html', cobot=info)

if __name__ == "__main__":
    app.run(host="128.237.237.136")
