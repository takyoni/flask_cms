import os

from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template_string, request
from dotenv import load_dotenv
import logging

logging.basicConfig(filename='record.log', level=logging.INFO)
load_dotenv(dotenv_path='../app.env')
DBUSER = os.getenv('DBUSER')
DBPASS = os.getenv('DBPASS')
DBHOST = os.getenv('DBHOST')
DBNAME = os.getenv('DBNAME')
database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=DBUSER,
    dbpass=DBPASS,
    dbhost=DBHOST,
    dbname=DBNAME
)

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)

# initialize database migration management
migrate = Migrate(app, db)


@app.route('/')
def view_registered_guests():
    from models import Guest
    guests = Guest.query.all()
    return render_template('guest_list.html', guests=guests)


@app.route('/register', methods=['GET'])
def view_registration_form():
    return render_template('guest_registration.html')


@app.route('/register', methods=['POST'])
def register_guest():
    from models import Guest
    name = request.form.get('name')
    email = request.form.get('email')

    guest = Guest(name, email)
    db.session.add(guest)
    db.session.commit()

    return render_template(
        'guest_confirmation.html', name=name, email=email)
#{{request.application.__globals__.__builtins__.__import__(%27os%27).popen(%27id%27).read()}}
@app.route("/welcome")
def home():
    user = request.args.get('user') or None

    template = '''
    <html><head>
    <title>Welcome</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
    integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css"
    integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
    integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous">
    </script><style>body {margin: 90px; background-image: url('{{url_for('static', filename='bg.jpg')}}');}</style></head><body>
    '''

    footer = '''
    <br><p style="margin-top: 30px;">
    '''

    if user == None:
        template = template + '''
        <h1>Search Form</h1>
        <form>
        <input type="text" class="form-control" id="namefield" name="user" aria-describedby="emailHelp" placeholder="Name" value="Username"><br>
        <input type="submit" value="Search" class="btn btn-default">
        </form>
        '''.format(user) + footer
    else:
        template = template + '''
        <h1>{}</h1>
        Welcome to the vulnerable app.<br>
        '''.format(user) + footer
    
    return render_template_string(template)
