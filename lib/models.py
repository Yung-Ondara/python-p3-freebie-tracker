from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # Relationships
    freebies = relationship('Freebie', back_populates='company')

    def __repr__(self):
        return f'<Company {self.name}>'

    # Method to give a freebie to a dev
    def give_freebie(self, dev, item_name, value):
        from models import Freebie  # if needed to avoid circular import
        new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return new_freebie

    @property
    def devs(self):
        return list({freebie.dev for freebie in self.freebies})

    @classmethod
    def oldest_company(cls):
        from sqlalchemy.orm import Session
        session = Session.object_session(cls)
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # Relationships
    freebies = relationship('Freebie', back_populates='dev')

    def __repr__(self):
        return f'<Dev {self.name}>'

    @property
    def companies(self):
        return list({freebie.company for freebie in self.freebies})

    def received_one(self, item_name):
        return any(f.item_name == item_name for f in self.freebies)

    def give_away(self, other_dev, freebie):
        if freebie.dev_id == self.id:
            freebie.dev = other_dev


class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    dev_id = Column(Integer, ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    # Relationships
    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')

    def __repr__(self):
        return f'<Freebie {self.item_name} (${self.value})>'

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
