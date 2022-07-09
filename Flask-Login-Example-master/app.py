"""Flask Login Example and serve membership card"""

from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from utils import get_member_data, getname
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        try:
            userid = session.get('name')
        except:
            userid = ''
        
        with open("data.json", encoding='utf-8') as fh:
            data = json.load(fh)
        if userid:
            cot = data[userid]["cotisation"]
            nom = data[userid]["nom"]
            prenom = data[userid]["prenom"]
            return render_template('index.html', id=userid, cot=cot, nom=nom, prenom=prenom)

        if request.method == 'POST':
            return render_template('index.html')
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(userid=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                session['name'] = name
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
        except:
            return redirect(url_for('login'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        new_user = User(
            userid=request.form['username'],
            password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    session['name'] = ''
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
    