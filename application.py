from flask import Flask, url_for
from flask import render_template
from flask import request



application = Flask(__name__)

@application.route('/')
def home():
    return render_template('home.html')

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@application.route('/job_seeker')
def job_seeker():
    return render_template('job_seeker.html')

@application.route('/job_poster')
def job_poster():
    return render_template('job_poster.html')


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()