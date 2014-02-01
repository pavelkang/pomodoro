# oauth_verifier is different every time E15F1E72E60D985F48AD6BFCF46D1F5E
# oauth_token is different
from flask import *
from functools import wraps
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from auth import *

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

@app.route('/test') # test URL
def test():
    return render_template('test.html')

@app.route('/new')
def new():
    return render_template('new.html')

@app.route('/App') # App URL
def App():
    messages = ["112", "122", "123", "132", "151"]
    return render_template('App.html', messages=messages, messages_range=range(len(messages)))
    """
    if "oauth_verifier" in request.url:
        authurl = request.url
        auth_token = get_auth_token(request_token, authurl)
        authorize_data = authorize(auth_token)
        session["auth_token"] = authorize_data[1]
        message = authorize_data[0]
        try:
            return render_template('App.html', messages=["112"])#message)
        except:
            flash(sys.exc_info()[0])
            # flash("I am running on Local")
    else:
        pass
    return render_template('App.html')
    """
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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('log'))

@app.route('/auth') # auth URL
def auth():
    url = None
    return render_template('auth.html', url=goto_auth_url)

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

if __name__ == "__main__":
    app.run(debug=True)
