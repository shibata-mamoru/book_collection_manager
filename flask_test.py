# -*- coding:utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('Camera_access_test.html',title='flask test')

@app.route('/bookdata',methods=["GET","POST"])
def test_post():
    print('POST')

    return 'Hello'

if __name__ == "__main__":
    app.run(debug=True)