# SQLAlchemy
## Úvod do SQLAlchemy
### Co to je SQLAlchemy?
SQLAlchemy je framewrok na komunikaci mezi Python a SQL, která umožňuje vývojářům přistupovat a spravovat databáze SQL pomocí jazyka Python. Práce s objekty poskytuje vývojářům flexibilitu a umožňuje jim vytvářet vysoce výkonné aplikace založené na SQL.
### Co to je ORM
Object Realtion Mapping (Objektově relační zobrazení) je programovací technika v softwarovém inženýrství, která zajišťuje automatickou konverzi dat mezi relační databází a objektově orientovaným programovacím jazykem.
### Instalace
````
pip install sqlalchemy
````
````
pip install mysqlclient
````
````
pip install mysql-connector-python
````
````
pip install flask
````
## 1. Část
### Tvorba databáze
### Base
````
Base = declarative_base()
````
- funkce používaná k vytvoření základní třídy, která slouží jako základ pro vytváření deklarativních tříd mapujících objekty na databázové tabulky

### Tabulka
class MyTable(Base):
	__tablename__ = 'my_table'


### Primární klíč
````
class MyTable(Base):
	__tablename__ = 'my_table'
	id = Column(Integer, primary_key=True, autoincrement=True)
````
- Primární klíč definuje hlavní a jedinečný identifikátor tabulky

### Text
````
class MyTable(Base):
	__tablename__ = 'my_table'
	id = Column(Integer, primary_key=True, autoincrement=True)
	text = Column(String(255))
````

### Datum
````
class MyTable(Base):
	__tablename__ = 'my_table'
	id = Column(Integer, primary_key=True, autoincrement=True)
	text = Column(String(255))
	birthdate = Column(Date)
````
- V SQLAlchemy se sloupec typu Date formátuje podle databázového systému nebo backendu
	- SQLite obvykle ukládá datum ve formátu 'YYYY-MM-DD'.
	- MySQL používá formát 'YYYY-MM-DD'.
	- PostgreSQL obvykle používá formát 'YYYY-MM-DD'.
	- Oracle může používat odlišný formát, například 'DD-MON-YYYY'.
	- SQL Server používá formát 'YYYY-MM-DD'.

### DateTime
````
class MyTable(Base):
	__tablename__ = 'my_table'
	id = Column(Integer, primary_key=True, autoincrement=True)
	text = Column(String(255))
	birthdate = Column(Date)
	created_at = Column(DateTime(timezone=True))
````
- DateTime sloupec v SQLAlchemy reprezentuje časový okamžik obsahující datum a čas a může být používán k ukládání hodnoty s informacemi o datumu a čase
- Formát je definován dle backendu
- 'timezone' -> Tento parametr umožňuje specifikovat, zda chcete pracovat s časy v lokálním časovém pásmu (True), v UTC (False), nebo se chcete postavit na svou vlastní správu časových pásem (tzinfo objekt).

### Defaultní hodnota
````
class MyTable(Base):
	__tablename__ = 'my_table'
	id = Column(Integer, primary_key=True, autoincrement=True)
	text = Column(String(255))
	birthdate = Column(Date)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
````
- V tomto případě jsme využili funkce, která nastaví defaultní hodnotu jako aktuální datum a čas

### Nastavení relace
````
class FirstTable(Base):
	__tablename__ = 'first_table'
	id = Column(Integer, primary_key=True, autoincrement=True)
	text = Column(String(255))
	birthdate = Column(Date)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	vztah = relationship("SecondTable")
	
class SecondTable(Base):
    __tablename__ = 'second_table'
    id = Column(Integer, primary_key=True)
    first_table_id = Column(Integer, ForeignKey('first_table.id'))
````
- Cizí klíč je identifikátor tabulky, který definuje relaci
- POZOR: Do vztahu píšeme Třídu do uvozovek, ale do cizího klíče už ne!
### 1. Úkol
Vytvořte databázi se třemi tabulkami o zákazníkovi:
- zakaznik
	- Id
 	- Jméno
 	- Příjmení
 	- Datum vytvoření
- zakaznik_kontakt
 	- Id
 	- Telefon
 	- Email
- zakaznik_adresa
 	- Id
 	- Ulice
 	- Město
 	- PSČ
 	- Trvalé bydliště (Ano/Ne)
 ````
from sqlalchemy import Column, Integer, String, DateTime, Enum, MetaData, func, create_engine, inspect
from sqlalchemy.orm import relationship, declarative_base
````
````
class Zakaznik(Base):
    __tablename__ = 'zakaznik'
    
    id_zak = Column(Integer, primary_key=True, autoincrement=True)
    jmeno = Column(String(25))
    prijmeni = Column(String(25))
    dt_create = Column(DateTime, server_default=func.now())
    
class ZakaznikContact(Base):
    __tablename__ = 'zakaznik_kontakt'
    
    id_zak_con = Column(Integer, primary_key=True, autoincrement=True)
    telefon = Column(String(9))
    email = Column(String(50))

class ZakaznikAdress(Base):
    __tablename__ = 'zakaznik_adresa'
    
    id_zak_adr = Column(Integer, primary_key=True, autoincrement=True)
    ulice = Column(String(40))
    mesto = Column(String(40))
    psc = Column(String(5))
    trvale_bydliste = Column(Enum("Y", "N"))
````
Kontrola zda se vše vytvořilo jak mělo:
````
def create_tables():
    # Vytvoření in-memory databáze
    engine = create_engine('sqlite:///:memory:', echo=True)

    # Vytvoření schématu (metadata) pro tabulky
    metadata = MetaData()

    # Vytvoření tabulek
    Base.metadata.create_all(engine)

    # Získání informací o tabulkách
    inspector = inspect(engine)

    # Získání názvů všech tabulek
    table_names = inspector.get_table_names()
    print(f"Seznam tabulek: {table_names}")
    
    for table_name in table_names:
        columns = inspector.get_columns(table_name)

    # Vytisknutí informací o sloupcích
        print()
        print(f"Struktura tabulky '{table_name}':")
        for column in columns:
            print(f"Název sloupce: {column['name']}, Typ sloupce: {column['type']}")
        print()

# Spuštění funkce
create_tables()
````
### 2. Úkol
Vytvořte relace mezi tabulkami o zákazníkovi:
- Vytvořte relaci v 'zakaznik'
- Vytvořte cizí klíče pro tabulku 'zakaznik_adresa' a 'zakaznik_kontakt'
````
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, MetaData, func, create_engine, inspect
from sqlalchemy.orm import relationship, declarative_base
````
````
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
````
Kontrola:
````
def create_tables():
    # Vytvoření in-memory databáze
    engine = create_engine('sqlite:///:memory:', echo=False)

    # Vytvoření schématu (metadata) pro tabulky
    metadata = MetaData()

    # Vytvoření tabulek
    Base.metadata.create_all(engine)

    # Získání informací o tabulkách
    inspector = inspect(engine)

    # Získání názvů všech tabulek
    table_names = inspector.get_table_names()
    print(f"Seznam tabulek: {table_names}")

    for table_name in table_names:
        # Získání informací o sloupcích
        columns = inspector.get_columns(table_name)

        # Vytisknutí informací o sloupcích
        print()
        print(f"Struktura tabulky '{table_name}':")
        for column in columns:
            print(f"Název sloupce: {column['name']}, Typ sloupce: {column['type']}")

        # Získání informací o klíčích
        primary_keys = inspector.get_pk_constraint(table_name)
        foreign_keys = inspector.get_foreign_keys(table_name)

        print(f"\nInformace o klíčích pro tabulku '{table_name}':")
        print("Primární klíče:")
        for pk in primary_keys['constrained_columns']:
            print(f" - {pk}")

        print("\nCizí klíče:")
        for fk in foreign_keys:
            print(f" - Sloupec: {fk['constrained_columns']}, Reference: {fk['referred_columns']}")

# Spuštění funkce
create_tables()
````
### Vkládání záznamů do tabulky
- Při vkládání dat do tabulky, je důležité znát typy sloupců a jejich omezení
	   
````
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Vytvoření spojení k databázi
engine = create_engine('sqlite:///:memory:')

# Vytvoření Session
Session = sessionmaker(bind=engine)
session = Session()

# Vytvoření nového záznamu
novy_zakaznik = Zakaznik(jmeno='John', prijmeni='Doe')

# Přidání nového záznamu do session
session.add(novy_zakaznik)

# Potvrzení změn (provedení commitu)
session.commit()
````
### 3. Úkol
- Přidejte 5 záznamů do:
	- 'zakaznik'
 	- 'zakaznik_kontakt'
	- 'zakaznik_adresa'
````
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
# Potvrzení změn (provedení commitu)
session.commit()
````
Kontrola:
````
session = Session()
zakaznici = session.query(Zakaznik).all()
session.commit()

for zakaznik in zakaznici:
    print(f"ID: {zakaznik.id_zak}, Jméno: {zakaznik.jmeno}, Příjmení: {zakaznik.prijmeni}, Datum vytvoření: {zakaznik.dt_create}")
    print("Kontakt:")
    for kontakt in zakaznik.kontakt:
        print(f"  Telefon: {kontakt.telefon}, Email: {kontakt.email}")
    print("Adresa:")
    for adresa in zakaznik.adresa:
        print(f"  Ulice: {adresa.ulice}, Město: {adresa.mesto}, PSČ: {adresa.psc}, Trvalé bydliště: {adresa.trvale_bydliste}")
    print()
````
### Selekce údajů z tabulky
- Nejčastější úlohou při práci s databází je vytažení údajů z nějaké tabulky -> <b>Select</b>
- V případě SQLAlchemy se využívá tato syntaxe
````
session = Session()
result = session.query(Trida_tabulky).all()
session.commit()
````
- Výpis pak provedme takto:
````
for row in result:
    print(row.sloupec1, row.sloupec2)
````
- Filtrování v selectu se využívá pomocí <b>WHERE</b> podmínky
- V SQLAlchemy vypadá syntaxe takto:
````
session = Session()
result = session.query(Trida_tabulky).filter(Trida_tabulky.sloupec == hodnota).all()
session.commit()
````
- Výpis pak provedme takto:
````
for row in result:
    print(row.sloupec1, row.sloupec2)
````
- Důlěžitým prvkem může být také seřazení záznamů -> <b>Order By</b>
- V SQLAlcehym vypadá syntaxe takto:
- Pro <b>ASCENDING</b>:
````
session = Session()
result = session.query(Trida_tabulky).order_by(Trida_tabulky.sloupec.asc()).all()
session.commit()
````
- Pro <b>DESCENDING</b>:
````
session = Session()
result = session.query(Trida_tabulky).order_by(Trida_tabulky.sloupec.desc()).all()
session.commit()
````
- Výpis pak provedme takto:
````
for row in result:
    print(row.sloupec1, row.sloupec2)
````
### 4. Úkol
- Vytvořte z tabulky:
	- 'zakaznik' -> select, který vybere vše a vypíše jméno a příjmení 
  	- 'zakaznik_adresa' -> select, který vybere pouze adresy trvalého bydliště a vypíše je
  	- 'zakaznik_kontakt' -> select, který vybere vše a vypíše emaily seřazené sestupně
````
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
````
- Kontrola:
````
for zakaznik in result:
    print(zakaznik.jmeno, zakaznik.prijmeni)
print()

for zakaznik in result2:
    print(zakaznik.mesto, zakaznik.psc)
print()

for zakaznik in result3:
    print(zakaznik.email, zakaznik.telefon)
print()
````
### Odstranění záznamů
- Někdy je potřeba nějaké záznamy smazat
- V SQLAlchemy vypadá syntaxe takto:
````
session = Session()
session.query(Trida_tabulky).filter(Trida_tabulky.sloupec == hodnota).delete()
session.commit()
````
### Úkol 5
- Smažte z tabulky 'zakaznik_adresa' všechny adresy, které nejsou trvalé
````
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
session.query(ZakaznikAdress).filter(ZakaznikAdress.trvale_bydliste == 'N').delete()
session.commit()
````
- Kontrola:
````
session = Session()
result1 = session.query(ZakaznikAdress).all()
session.commit()

for zakaznik in result1:
    print(zakaznik.mesto, zakaznik.ulice)
print()
````
### Updatování hodnot
- Pro některé úkony je třeba aktualizovat hodnoty
- Slouží pro to syntaxe:

````
session = Session()
session.query(Trida_tabulky).filter(Trida_tabulky.sloupec == 'hodnota').update({"měněný sloupec": 'Nová hodnota'})
session.commit()
````
### 6. Úkol
- Uprave sloupec 'ulice' v tabulce 'zakaznik_adresa':
	- Pokud je město 'Cityville' -> ulice bude 'Nová ulice'
````
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

session.query(ZakaznikAdress).filter(ZakaznikAdress.mesto == 'Cityville').update({"ulice": 'Nová ulice'})
session.commit()
````
- Kontrola:
````
session = Session()
result1 = session.query(ZakaznikAdress).all()
session.commit()
for zakaznik in result1:
    print(zakaznik.mesto, zakaznik.ulice)
print()
result1 = session.query(ZakaznikAdress).all()
````
## 2. Část
### Databáze
Naše databáze, kterou budeme používat, je velice jednoduchou simulací bankovního prostředí pro úvěry
### ERD
![alt text](https://github.com/Hamzic12/SQL-Alchemy/blob/main/ERD.png)
### Tabulky
#### <b>CUSTOMER</b>
Tabulka klientů a jejich základní informace
- <i>customer_id</i> = Identifikátor klienta
- <i>name</i> = Jméno klienta
- <i>surname</i> = Příjmení klienta
- <i>active_flag</i> = Označení zda je klient aktivní
#### <b>CUSTOMER_ADDRESS</b>
Tabulka adres klientů</i>
- <i>customer_address_id</i> = Identifikátor adresy
- <i>psc</i> = PSČ 
- <i>city</i> = Město
- <i>street</i> = Ulice
- <i>number</i> = Číslo domu
- <i>domicile_flag</i> = Označení zda je to adresa trvalého bydliště
- <i>customer_id</i> = Idenfitikátor klienta
#### <b>CUSTOMER_CONTACT</b>
Tabulka kontaktů na klienty
- <i>customer_contact_id</i> = Idenfitifkátor kontaktu
- <i>phone</i> = Telefonní číslo
- <i>email</i> = Email
- <i>customer_id</i> = Identifikátor klienta
#### <b>ACCOUNT</b>
Tabulka účtů a informace o nich
- <i>account_id</i> = Identifikátor účtu
- <i>acc_type</i> = Typ účtu
- <i>acc_balance</i> = Zůstatek
- <i>active_flag</i> = Označení zda je účet aktivní
- <i>customer_id</i> = Identifikátor klienta
#### <b>BANK_USER</b>
Tabulka zaměsntanců a jejich základní informace
- <i>bank_user_id</i> = Identifikátor zaměstnance
- <i>name</i> = Jméno zaměstnance
- <i>surname</i> = Příjmení zaměstnance
- <i>active_flag</i> = Označení zda je zaměstnanec aktivní
#### <b>BANK_USER_ADDRESS</b>
Tabulka adres zaměstnanců 
- <i>bank_user_adr_id</i> = Identifikátor adresy 
- <i>psc</i> = PSČ
- <i>city</i> = Město
- <i>street</i> = Ulice
- <i>number</i> = Číslo domu
- <i>domicile_flag</i> = Označení zda je to adresa trvalého bydliště
- <i>bank_user_id</i> = Identifikátor zaměstnance
#### <b>BANK_USER_CONTACT</b>
Tabulka kontaktů na zaměstnance
- <i>bank_user_contact_id</i> = Identifikátor kontaktu
- <i>phone_work</i> = Pracovní telefonní číslo
- <i>email_work</i> = Pracovní email
- <i>phone_personal</i> = Osobní telefonní číslo
- <i>email_personal</i> = Osobní email
- <i>bank_user_id</i> = Identifikátor zaměstnance
#### <b>LOAN_UNPAYED</b>
Tabulka aktivních úvěrů a jejich informace
- <i>loan_id</i> = Identifikátor úvěru
- <i>loan_type</i> = Typ úvěru
- <i>rem_instalment</i> = Zbývající počet splátek
- <i>instalment</i> = Celková výše úvěru
- <i>month_instalment</i> = Měsíční výše splátky
- <i>account_id</i> = Identifikátor účtu
- <i>bank_user_id</i> = Identifikátor zaměstnance, který úvěr sjednal
#### <b>LOAN_PAYED</b>
Tabulka splacených úverů
- <i>loan_hist_id</i> = Identifikace splaceného úvěru
- <i>loan_type</i> = Typ úvěru
- <i>instalment</i> = Výše úvěru
- <i>account_id</i> = Identifikátor účtu

### <b>Základy</b>
Engine slouží k připojení k databazi a k průběhu SQL příkazů. Ve funkci create_engine je string parametr, jejiž obsahem je:
- dialect = druh databáze
- driver = DBAPI
- username = uživatelské jméno
- password = heslo
- host = Vetšinou to bývá Ip adresa
- port = jaký port
- database = jakou databázi
````
engine = create_engine('<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>', echo=True)
````

declarative_base slouží k vytváření modelů.
````
Base = declarative_base()
````

Tabulka, je třída, která dědí z objektu Base.
````
class Table1(Base):
    __tablename__ = 'Tabel1'

    id = Column(Integer, primary_key=True, nullable=False)
    column1 = Column(String)
    column2 = Column(Integer)
    column3 = Column(Date)
    
    table2_id = relationship(Integer, foreign_keys='Table2.id') #one to many
    #one to many
````

A nakonec k vytvořeni databáze a všechny tabulky.
````
Base.metadata.create_all(engine)
````

### Úkol č. 1:
Vytvořte databázi s třemi tabulkami zákzaníkovi(tabulka1=id, jméno, příjmení | tabulka2=id, telefon, email | tabulka3=id, ulice, mesto, psc).

### Úkol č. 2:
Vytvořte funkci, ktera najde kolik zákazníku bydlí na vámi vybrané PSČ. 

### Úkol č. 3:

### Úkol č. 4:

### Úkol č. 5:
