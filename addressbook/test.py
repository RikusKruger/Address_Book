from contacts import Contact

contact = Contact.query.filter_by(name='Rikus').first()
print(contact)