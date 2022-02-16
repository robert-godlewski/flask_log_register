from flask_app import app
from flask_app.models.user import User
from flask import render_template, redirect, session, request
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def counter(): return render_template("index.html")

@app.route('/dashboard')
def dashboard(): 
    data = {
        "id": session['id']
    }
    return render_template("dashboard.html", user=User.get_one(data))

@app.route('/user/register', methods=['POST'])
def register():
    if not User.validate_user(request.form): return redirect('/')
    print(f"Password: {request.form['password']}")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(f"Hashed Password: {pw_hash}")
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,
    }
    user_id = User.save(data)
    session['id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login(): 
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/logout', methods=['POST'])
def logout(): return None
