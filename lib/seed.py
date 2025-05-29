#!/usr/bin/env python3

from your_app import app, db
from models import Dev, Company, Freebie

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create devs and companies
    dev1 = Dev(name="Alice")
    dev2 = Dev(name="Bob")

    company1 = Company(name="TechCorp")
    company2 = Company(name="InnovateX")

    db.session.add_all([dev1, dev2, company1, company2])
    db.session.commit()

    # Create freebies
    freebie1 = Freebie(item_name="Sticker Pack", value=5, dev_id=dev1.id, company_id=company1.id)
    freebie2 = Freebie(item_name="T-Shirt", value=20, dev_id=dev2.id, company_id=company2.id)

    db.session.add_all([freebie1, freebie2])
    db.session.commit()

    print("Database seeded successfully.")
