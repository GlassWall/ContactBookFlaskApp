import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "contacts.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(80), unique=False, nullable=False)
    LastName = db.Column(db.String(80), unique=False, nullable=False)
    Phone = db.Column(db.String(20), unique=False, nullable=False)
    Email =db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
    def __repr__(self):
        return "<FirstName: {} \n LastName:{} \n Phone:{} \n Email:{}>".format(self.FirstName,self.LastName,self.Phone, self.Email)


@app.route("/", methods=["GET", "POST"])
def home():
    contact = Contact(FirstName=request.form.get("FirstName"), LastName=request.form.get("LastName"),
                      Phone=request.form.get("Phone"), Email=request.form.get("Email"))

    if request.form:
        db.session.add(contact)
        db.session.commit()
    contacts = contact.query.all()
    print(contacts)
    return render_template("home.html", contacts=contacts)

@app.route("/searchByEmail", methods=["GET", "POST"])
def search():
    if request.form:
        contact = Contact.query.filter_by(Email=request.form.get("Email"))
        print(contact)
        return render_template("searchByEmail.html", contacts=contact)
    return render_template("searchByEmail.html")

@app.route("/searchByName", methods=["GET", "POST"])
def searchByName():
    if request.form:
        contact = Contact.query.filter_by(FirstName=request.form.get("FirstName"))
        print(contact)
        return render_template("searchByName.html", contacts=contact)
    return render_template("searchByName.html")


@app.route("/update", methods=["POST"])
def update():
    newEmail = request.form.get("newEmail")
    oldEmail = request.form.get("oldEmail")
    newLName = request.form.get("newLName")
    newPhone = request.form.get("newPhone")
    newFName = request.form.get("newFName")
    contact = Contact.query.filter_by(Email=oldEmail).first()
    contact.FirstName = newFName
    contact.LastName = newLName
    contact.Email = newEmail
    contact.Phone = newPhone
    db.session.commit()
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    email = request.form.get("Email")

    print(email)
    contact = Contact.query.filter_by(Email=email).first()
    print(contact)
    db.session.delete(contact)
    db.session.commit()
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)