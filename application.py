from flask import Flask, url_for
from flask import render_template
from flask import request, redirect
from docusign import embedded_signing_ceremony



application = Flask(__name__)

@application.route('/')
def home():
    return render_template('home.html')

@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@application.route('/job_seeker', methods=['GET', 'POST'])
def job_seeker():
    if request.method == 'POST':
        return redirect(embedded_signing_ceremony(), code=302)

    elif request.method == 'GET':
        return render_template('job_seeker.html', url = request.url)

@application.route('/job_poster', methods=['GET', 'POST'])
def job_poster():
    if request.method == 'POST':
        job_type = request.form['job_type']
        return redirect(url_for('job_detail',job_type=job_type))

    elif request.method == 'GET':
        return render_template('job_poster.html')

@application.route('/job_detail/<job_type>', methods=['GET', 'POST'])
def job_detail(job_type=None):
    if request.method == 'POST':
        return redirect(url_for('thank_you_poster'))

    elif request.method == 'GET':
        return render_template('job_detail.html',job_type=job_type)

@application.route('/thank_you_poster', methods=['GET', 'POST'])
def thank_you_poster():
    return render_template('thank_you_poster.html')

@application.route('/thank_you_seeker', methods=['GET', 'POST'])
def thank_you_seeker():
    return render_template('thank_you_seeker.html')





if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
