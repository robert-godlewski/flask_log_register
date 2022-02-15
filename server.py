from flask import render_template, redirect, session, request
from flask_app import app

@app.route('/')
def counter(): return render_template("index.html")


if __name__ == "__main__": app.run(debug=True, port=8000)
