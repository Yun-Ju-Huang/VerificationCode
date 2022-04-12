# from crypt import methods
# from curses import meta
from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

# @app.route('/user/<name>')
# def user(name):
#     return render_template('home.html',name = name)

@app.route('/home')
def user():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()