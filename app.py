from flask import Flask, redirect, render_template, request
from db import db_session as db , User
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = db.query(User).filter(User.username == request.form['username']).first()
        if user is None or user.password != request.form['password']:
            return render_template('index.html', error="Invalid username or password")
        if user.password == request.form['password']:
            return 'Logged in'
    else:
        return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = db.query(User).filter(User.username == request.form['username']).first()
        if user is not None:
            return render_template('signup.html', username_error="Username already exists")
        if request.form['password'] != request.form['confirmpassword']:
            return render_template('signup.html', confirmpassword_error="Passwords do not match")
        user = User(username=request.form['username'], password=request.form['password'])
        db.add(user)
        db.commit()
        return redirect('/')
    else:
        return render_template('signup.html', message="Important")

@app.route('/reset', methods=['POST', 'GET'])
def reset():
    if request.method == 'POST':
        user = db.query(User).filter(User.username == request.form['username']).first()
        if user is None:
            return render_template('forgot.html', username_error="Username does not exist")
        if request.form['password'] != request.form['confirmpassword']:
            return render_template('forgot.html', confirmpassword_error="Passwords do not match")
        user.password = request.form['password']
        db.commit()
        return redirect('/')
    else:
        return render_template('forgot.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
