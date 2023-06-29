#!/usr/bin/env python3
'''Basic flask application'''


from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    '''home page'''
    return render_template('0-index.html')


if __name == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
