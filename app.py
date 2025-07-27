from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Python!'

@app.route('/about')
def about():
    return 'This is the about page'
