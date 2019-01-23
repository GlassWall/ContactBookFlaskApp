import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
from flask_paginate import Pagination, get_page_args

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "contacts.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

users = list(range(100))

def get_users(offset=0, per_page=10):
    return users[offset: offset + per_page]

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(80), unique=False, nullable=False)
    LastName = db.Column(db.String(80), unique=False, nullable=False)
    Phone = db.Column(db.String(20), unique=False, nullable=False)
    Email =db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
    def __repr__(self):
        return "<FirstName: {} \n LastName:{} \n Phone:{} \n Email:{}>".format(self.FirstName,self.LastName,self.Phone, self.Email)


@app.route('/searchByEmail', methods=["GET","POST"])
def searchByEmail():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(users)

    pagination_users = get_users(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    if request.form:
        email = request.form.get("Email")
        if email != "":
            contact = Contact.query.filter(Contact.Email.like("%{}%".format(email))).all()
        else:
            contact= []
        print(type(contact))
        return render_template('searchByEmail.html',
                               users=contact,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               )
    return render_template('searchByEmail.html',
                           users=[],
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@app.route('/searchByName', methods=["GET","POST"])
def searchByName():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(users)

    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    if request.form:
        firstName = request.form.get("FirstName")
        if firstName != "":
            contact = Contact.query.filter(Contact.Email.like("%{}%".format(firstName))).all()
        else:
            contact = []
        return render_template('searchByName.html',
                               users=contact,
                               page=page,
                               per_page=per_page,
                               pagination=pagination,
                               )
    return render_template('searchByName.html',
                           users=[],
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


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