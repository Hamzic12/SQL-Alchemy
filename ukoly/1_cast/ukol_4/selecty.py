from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Zakaznik(Base):
    __tablename__ = 'zakaznik'
    
    id_zak = Column(Integer, primary_key=True, autoincrement=True)
    jmeno = Column(String(25))
    prijmeni = Column(String(25))
    dt_create = Column(DateTime, server_default=func.now())
    
    kontakt = relationship("ZakaznikContact")
    adresa = relationship("ZakaznikAdress")
    
    
class ZakaznikContact(Base):
    __tablename__ = 'zakaznik_kontakt'
    
    id_zak_con = Column(Integer, primary_key=True, autoincrement=True)
    telefon = Column(String(9))
    email = Column(String(50))
    
    id_zak = Column(Integer, ForeignKey('zakaznik.id_zak'))

class ZakaznikAdress(Base):
    __tablename__ = 'zakaznik_adresa'
    
    id_zak_adr = Column(Integer, primary_key=True, autoincrement=True)
    ulice = Column(String(40))
    mesto = Column(String(40))
    psc = Column(String(5))
    trvale_bydliste = Column(Enum("Y", "N"))
    
    id_zak = Column(Integer, ForeignKey('zakaznik.id_zak'))

# Vytvoření spojení k databázi
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)  # Vytvoření tabulek

Session = sessionmaker(bind=engine)
session = Session()

novi_zakaznici = [
    Zakaznik(jmeno='John', prijmeni='Doe'),
    Zakaznik(jmeno='Alice', prijmeni='Smith'),
    Zakaznik(jmeno='Bob', prijmeni='Johnson'),
    Zakaznik(jmeno='Eva', prijmeni='Brown'),
    Zakaznik(jmeno='David', prijmeni='Miller')
]

session.add_all(novi_zakaznici)

nove_kontakty = [
    ZakaznikContact(telefon='123456789', email='john.doe@example.com', id_zak=1),
    ZakaznikContact(telefon='987654321', email='alice.smith@example.com', id_zak=2),
    ZakaznikContact(telefon='555444333', email='bob.johnson@example.com', id_zak=3),
    ZakaznikContact(telefon='111222333', email='eva.brown@example.com', id_zak=4),
    ZakaznikContact(telefon='999888777', email='david.miller@example.com', id_zak=5)
]

session.add_all(nove_kontakty)

nove_adresy = [
    ZakaznikAdress(ulice='Main Street', mesto='Cityville', psc='12345', trvale_bydliste='Y', id_zak=1),
    ZakaznikAdress(ulice='Maple Avenue', mesto='Townsville', psc='54321', trvale_bydliste='N', id_zak=2),
    ZakaznikAdress(ulice='Oak Street', mesto='Villageton', psc='98765', trvale_bydliste='Y', id_zak=3),
    ZakaznikAdress(ulice='Cedar Road', mesto='Hamletville', psc='13579', trvale_bydliste='N', id_zak=4),
    ZakaznikAdress(ulice='Pine Lane', mesto='Burgville', psc='24680', trvale_bydliste='Y', id_zak=5)
]
session.add_all(nove_adresy)
session.commit()


session = Session()

result = session.query(Zakaznik).all()
result2 = session.query(ZakaznikAdress).filter(ZakaznikAdress.trvale_bydliste == 'Y').all()
result3 = session.query(ZakaznikContact).order_by(ZakaznikContact.email.desc()).all()

session.commit()


for zakaznik in result:
    print(zakaznik.jmeno, zakaznik.prijmeni)
print()

for zakaznik in result2:
    print(zakaznik.mesto, zakaznik.psc)
print()

for zakaznik in result3:
    print(zakaznik.email, zakaznik.telefon)
print()




