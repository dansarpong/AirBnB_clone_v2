#!/usr/bin/python3
'''
A simple Flask web application
'''
from flask import Flask


'''The Flask application instance'''
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    '''The home page'''
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    '''The hbnb page'''
    return 'HBNB'


@app.route('/c/<text>')
def cisfun(text):
    '''The C page'''
    return 'C ' + text.replace('_', ' ')


@app.route('/python')
@app.route('/python/<text>')
def pythoniscool(text="is cool"):
    '''The Python page'''
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<int:n>')
def number(n):
    '''The numbers page'''
    return '{:d} is a number'.format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
