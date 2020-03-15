import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from sqlalchemy.orm import relationship

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "contactdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    num = db.Column(db.String(80))
    email = db.Column(db.String(80))

    def __repr__(self):
        return "<Name: {}>".format(self.name)


# class Email(db.Model):
#     __tablename__ = 'emails'
#     id = db.Column(db.Integer, primary_key=True)
#     email_address = db.Column(db.String(80))
#     contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
#     contact = relationship("Contact", back_populates="emails")
#
#     def __repr__(self):
#         return self.email_address


# Contact.emails = relationship('Email', order_by=Email.id, back_populates="contact")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        entry = Contact(name=request.form.get("name"),
                        num=request.form.get("num"),
                        surname=request.form.get("surname"),
                        email=request.form.get("email"))

        # entry.email = Email(email_address=request.form.get("email"))
        db.session.add(entry)
        db.session.commit()

    contacts = Contact.query.all()
    return render_template("home.html", contacts=contacts)


@app.route("/update", methods=["POST"])
def update():
    new_name = request.form.get("new_name")
    old_name = request.form.get("old_name")
    contacts = Contact.query.filter_by(name=old_name).all()
    for contact in contacts:
        contact.name = new_name
    db.session.commit()
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
def search():
    try:
        searched = request.form.get("search")
        found = Contact.query.filter_by(name=searched)
        return render_template("home.html", contacts=found)
    except:
        return 'Contact does not exist'


#
@app.route("/reset", methods=["POST"])
def reset():
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    try:
        name = request.form.get("name")
        contact = Contact.query.filter_by(name=name).first()
        db.session.delete(contact)
        db.session.commit()
        return redirect("/")
    except:
        return 'Contact does not exist'


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
