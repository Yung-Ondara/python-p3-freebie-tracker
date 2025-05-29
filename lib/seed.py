from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Dev, Company
from models import Freebie 

# Replace with your database URI
engine = create_engine('sqlite:///freebies.db')  # or 'postgresql://user:pass@localhost/dbname'
Session = sessionmaker(bind=engine)
session = Session()

# Drop and recreate all tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Create Companies
company1 = Company(name="TechCorp", founding_year=2000)
company2 = Company(name="InnovateX", founding_year=1995)

# Create Devs
dev1 = Dev(name="Alice")
dev2 = Dev(name="Bob")
dev3 = Dev(name="Charlie")

# Add them to the session
session.add_all([company1, company2, dev1, dev2, dev3])
session.commit()

# Use give_freebie and commit each one
freebie1 = company1.give_freebie(dev1, item_name="T-Shirt", value=25)
freebie2 = company1.give_freebie(dev2, item_name="Water Bottle", value=15)
freebie3 = company2.give_freebie(dev1, item_name="Sticker Pack", value=5)
freebie4 = company2.give_freebie(dev3, item_name="Laptop Bag", value=50)

# Add the freebies and commit
session.add_all([freebie1, freebie2, freebie3, freebie4])
session.commit()

print("Seeded the database with sample Devs, Companies, and Freebies!")
