from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import mysql.connector

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    surname = Column(String(46), nullable=False)
    active_flag = Column(Enum('Y', 'N'), nullable=False, default='Y', server_default='Y')
    
    __table_args__ = (
        UniqueConstraint('customer_id', name='customer_id_UNIQUE'),
    )

class Account(Base):
    __tablename__ = 'account'

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    acc_type = Column(Enum('STANDARD', 'PLUS'), nullable=False)
    account_number = Column(Integer, nullable=False)
    acc_balance = Column(Integer, nullable=False)
    active_flag = Column(Enum('Y', 'N'), nullable=False, default='Y', server_default='Y')
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('account_id', name='account_id_UNIQUE'),
    )
    customer = relationship('Customer', backref='accounts')

class BankUser(Base):
    __tablename__ = 'bank_user'

    bank_user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    surname = Column(String(46), nullable=False)
    active_flag = Column(Enum('Y', 'N'), nullable=False, default='Y', server_default='Y')
    
    __table_args__ = (
        UniqueConstraint('bank_user_id', name='bank_user_id_UNIQUE'),
    )

class LoanUnpayed(Base):
    __tablename__ = 'loan_unpayed'

    loan_id = Column(Integer, primary_key=True, autoincrement=True)
    loan_type = Column(Enum('AUTO', 'HYPO', 'INVEST'), nullable=False)
    rem_instalment = Column(Integer, nullable=False)
    instalment = Column(Integer, nullable=False)
    month_instalment = Column(Integer, nullable=False)
    account_id = Column(Integer, ForeignKey('account.account_id'), nullable=False)
    bank_user_id = Column(Integer, ForeignKey('bank_user.bank_user_id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('loan_id', name='loan_id_UNIQUE'),
    )
    account = relationship('Account', backref='loans_unpayed')
    bank_user = relationship('BankUser', backref='loans_unpayed')

class BankUserContact(Base):
    __tablename__ = 'bank_user_contact'

    bank_user_contact_id = Column(Integer, primary_key=True, autoincrement=True)
    phone_work = Column(String(13), nullable=False)
    email_work = Column(String(70), nullable=False)
    phone_personal = Column(String(20), nullable=False)
    email_personal = Column(String(70))
    bank_user_id = Column(Integer, ForeignKey('bank_user.bank_user_id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('bank_user_contact_id', name='bank_user_contact_id_UNIQUE'),
    )
    bank_user = relationship('BankUser', backref='contact_info')

class BankUserAddress(Base):
    __tablename__ = 'bank_user_address'

    bank_user_adr_id = Column(Integer, primary_key=True, autoincrement=True)
    psc = Column(String(5), nullable=False)
    city = Column(String(34), nullable=False)
    street = Column(String(41), nullable=False)
    number = Column(String(7), nullable=False)
    domicile_flag = Column(Enum('Y', 'N'), nullable=False)
    bank_user_id = Column(Integer, ForeignKey('bank_user.bank_user_id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('bank_user_adr_id', name='bank_user_adr_id_UNIQUE'),
    )
    bank_user = relationship('BankUser', backref='addresses')

class CustomerAddress(Base):
    __tablename__ = 'customer_address'

    customer_address_id = Column(Integer, primary_key=True, autoincrement=True)
    psc = Column(String(5), nullable=False)
    city = Column(String(34), nullable=False)
    street = Column(String(41), nullable=False)
    number = Column(String(7), nullable=False)
    domicile_flag = Column(Enum('Y', 'N'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('customer_address_id', name='customer_address_id_UNIQUE'),
    )
    customer = relationship('Customer', backref='addresses')

class CustomerContact(Base):
    __tablename__ = 'customer_contact'

    customer_contact_id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(20), nullable=False)
    email = Column(String(70), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('customer_contact_id', name='customer_contact_id_UNIQUE'),
    )
    customer = relationship('Customer', backref='contacts')

class LoanPayed(Base):
    __tablename__ = 'loan_payed'

    loan_hist_id = Column(Integer, primary_key=True, autoincrement=True)
    loan_type = Column(Enum('AUTO', 'HYPO', 'INVEST'), nullable=False)
    instalment = Column(Integer, nullable=False)
    account_id = Column(Integer, ForeignKey('account.account_id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('loan_hist_id', name='loan_hist_id_UNIQUE'),
    )
    account = relationship('Account', backref='loans_payed')

def vytvor():
    # Připojení k MySQL serveru
    connection = mysql.connector.connect(
        host='mariadb',
        user='root',
        password='secret',
        port='3306'
    )

    # Vytvoření objektu cursor pro provádění SQL příkazů
    cursor = connection.cursor()

        # Vytvoření nové databáze (pokud neexistuje)
    database_name = 'mydb'
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

        # Uzavření cursoru a připojení
    cursor.close()
    connection.close()

        # Připojení k Mariadb a vytvoření tabulek
    engine = create_engine('mysql+mysqlconnector://root:secret@mariadb:3306/mydb', echo=True)
    Base.metadata.create_all(engine)

