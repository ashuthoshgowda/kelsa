from flask import Flask, url_for
from flask import render_template
from flask import request, redirect, flash
from docusign import embedded_signing_ceremony
from config import Config
from forms import JobPosterform
from datetime import datetime, timedelta
from db_setup import init_db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random

init_db()


application = Flask(__name__)
application.config.from_object(Config)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(application)

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
        tasks = [{"name":"Monica",
        "rate":45,
        "job_type":"Garderner",
        "jd":"Mow the lawn - 14ft * 20ft"},
        {"name":"Erica",
        "rate":30,
        "job_type":"Cook",
        "jd":"Cook Chicken Tikka Masala for the Party of 5"},
        {"name":"Rita",
        "rate":25,
        "job_type":"Driver",
        "jd":"Drive my car from the Downtown Bar"},
        {"name":"Tina",
        "rate":35,
        "job_type":"Garderner",
        "jd":"Mow the lawn - 14ft * 20ft"}]

        task = random.choice(tasks)
        print(task)
        return render_template('job_seeker.html',task=task, url = request.url)

@application.route('/job_poster', methods=['GET', 'POST'])
def job_poster():
    if request.method == 'POST':
        print(request.form)
        return redirect(url_for('thank_you_poster'))

    elif request.method == 'GET':
        t = datetime.now()
        hour = t.replace(second=0, microsecond=0, minute=0, hour=t.hour)+timedelta(hours=t.minute//30)
        return render_template('job_poster.html', hour = hour.hour)

@application.route('/job_detail/<job_type>', methods=['GET', 'POST'])
def job_detail(job_type=None, invalid_args=False):
    form = JobPosterform()

    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Job description - {}'.format(
                form.job_description.data))
            return redirect(url_for('thank_you_poster'))
        else:
            flash('Please enter valid data!')
            #return redirect('/index')
            return render_template('job_detail.html',job_type=job_type, form=form, invalid_args=True)
    elif request.method == 'GET':
        return render_template('job_detail.html',job_type=job_type, form=form, invalid_args=invalid_args)

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
