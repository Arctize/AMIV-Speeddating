#!/usr/bin/env python3

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from apps.models import Participants, TimeSlots
from sqlalchemy import create_engine
import requests
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@localhost/Speeddating'
db = SQLAlchemy(app)

#eng = create_engine('mysql+pymysql://root:toor@localhost/Speeddating')
#q = eng.execute('SHOW DATABASES')
#available_tables = q.fetchall()
#print(q)
for instance in db.session.query(Participants).order_by(Participants.id):
    print(instance.id, instance.Prename)

query = db.session.query(Participants.Prename).order_by(Participants.id)
print(query.all())

# Creates tables only when they don't already exist so we can just leave this here
db.create_all()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        result = request.form

        # Send POST request with parameters 'username' and 'password'. Verification has to be off since
        # SSL certs are self-signed.
        ack = requests.post("https://amiv-apidev.vsos.ethz.ch/sessions", data={"username" : str(result['nethz']), "password" : str(result['password'])}, verify=False)

        if ack.status_code == 201:
            return render_template("admin.html")
        return render_template('login.html')
    return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':

        year = None
        result = None
        prename = None
        name = None
        mobile = None
        address = None
        email = None
        age = None
        gender = None

        try:
            year = datetime.datetime.now().year
            result = request.form
            prename = str(result['prename'])
            assert(len(prename) > 0)

            name = str(result['name'])
            assert(len(name) > 0)

            mobile = str(result['mobile'])
            assert(len(mobile) > 0)

            address = str(result['address'])
            assert(len(address) > 0)

            email = str(result['mail'])
            assert(len(mail) > 0)

            age = int(result['age'])
            gender = bool(result['gender'])

        except (AssertionError, ValueError) as e:
            print(e)

            # TODO: Show actual error instead of redirectiing to an error page
            return render_template('signup.html', retry=True, prename=prename, name=name, mobile=mobile, address=address, email=email, age=age, gender=gender)

        admin = Participants(name, prename, email, mobile, address, age, gender, year)
        db.session.add(admin)
        db.session.commit()

        return render_template('success.html')

    return render_template('signup.html')



if __name__ == '__main__':
    app.run()
