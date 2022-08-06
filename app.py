from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///khelo.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Khelo(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(25), nullable=False)
    phn = db.Column(db.String(25), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.no} - {self.name}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        name = request.form['name']
        phn = request.form['phn']
        mail = request.form['mail']
        khelo = Khelo(name=name, phn=phn, mail=mail)
        db.session.add(khelo)
        db.session.commit()
    allp = Khelo.query.all()
    print(allp)
    return render_template('index.html',allp=allp)


@app.route('/show')
def show():
    allp = Khelo.query.all()
    print(allp) 
    return "Hello, Katy!"

@app.route('/update/<int:no>',methods=['GET','POST'])
def update(no):
    if request.method=='POST':
        name = request.form['name']
        phn = request.form['phn']
        mail = request.form['mail']
        p = Khelo.query.filter_by(no=no).first()
        p.name=name
        p.phn=phn
        p.mail=mail
        db.session.add(p)
        db.session.commit()
        return redirect("/")

    p = Khelo.query.filter_by(no=no).first()
    return render_template('update.html',p=p)

@app.route('/delete/<int:no>')
def delete(no):
    p = Khelo.query.filter_by(no=no).first()
    db.session.delete(p)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True, port=3000)
                     