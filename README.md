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
## 1. Část
### Tvorba databáze

### <b>Základy</b>

````
from sqlalchemy import Column, Integer, String, DateTime, Enum, MetaData, func, create_engine, inspect
from sqlalchemy.orm import relationship, declarative_base
````
````
engine = create_engine('<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>', echo=True)
````

Engine slouží k připojení k databázi a k průběhu SQL příkazů. Ve funkci create_engine je string parametr, jehož obsahem je:
- dialect = druh databáze
- driver = DBAPI
- username = uživatelské jméno
- password = heslo
- host = Vetšinou to bývá Ip adresa
- port = jaký port
- database = jakou databázi

### Base
````
Base = declarative_base()
````
Funkce slouží k vytvoření abstraktní třídy, která slouží k jednotnému vytváření deklarativních tříd mapujících objekty na databázové tabulky.

### Tabulka
class MyTable(Base):
	__tablename__ = 'my_table'


### Primární klíč
````
class MyTable(Base):
	__tablename__ = 'my_table'
	id = Column(Integer, primary_key=True, autoincrement=True)
````
Primární klíč definuje hlavní a jedinečný identifikátor tabulky.

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
V SQLAlchemy se sloupec typu Date formátuje podle databázového systému nebo backendu:
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
- DateTime sloupec v SQLAlchemy reprezentuje časový okamžik obsahující datum a čas.
- Formát je definován dle backendu.
- Parametr `timezone` umožňuje specifikovat, zda chcete pracovat s časy v lokálním časovém pásmu (True), v UTC (False), nebo se chcete postavit na svou vlastní správu časových pásem (tzinfo objekt).

### Výchozí hodnota
````
class MyTable(Base):
	__tablename__ = 'my_table'
	id = Column(Integer, primary_key=True, autoincrement=True)
	text = Column(String(255))
	birthdate = Column(Date)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
````
V tomto případě jsme využili funkce, která nastaví výchozí hodnotu jako aktuální datum a čas.

### Nastavení relací
1:N
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
1:1
````
class Osoba(Base):
    __tablename__ = "osoba"
    
    id = Column(Integer, primary_key=True)
    jmeno = Column(String(255))
    
    rodny_list_id = Column(Integer, ForeignKey("rodny_list.id"))
    rodny_list = relationship("RodnyList", uselist=False)

class RodnyList(Base):
    __tablename__ = "rodny_list"
    
    id = Column(Integer, primary_key=True)
    cislo = Column(String(10))
    osoba_id = Column(Integer, ForeignKey("osoba.id"))
````
M:N
````
class Osoba(Base):
    __tablename__ = "osoba"
    
    id = Column(Integer, primary_key=True)
    jmeno = Column(String(255))
    
    konicky = relationship("Konicek", secondary="osoba_konicek")

class Konicek(Base):
    __tablename__ = "konicek"
    
    id = Column(Integer, primary_key=True)
    nazev = Column(String(255))
    
    osoby = relationship("Osoba", secondary="osoba_konicek")

osoba_konicek = Table(
    "osoba_konicek",
    Base.metadata,
    Column("osoba_id", Integer, ForeignKey("osoba.id")),
    Column("konicek_id", Integer, ForeignKey("konicek.id")),
)
````
Cizí klíč je identifikátor tabulky, který definuje relaci.
- **POZOR:** Do vztahu píšeme Třídu do uvozovek, ale do cizího klíče už ne!
### 1.1 Úkol
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
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, MetaData, func, create_engine, inspect
from sqlalchemy.orm import relationship, declarative_base
````

Vytvoření databáze a tabulek:
````
engine = create_engine('sqlite:///:memory:', echo=False)

# Vytvoření schématu (metadat) pro tabulky
metadata = MetaData()

# Vytvoření tabulek
Base.metadata.create_all(engine)
````
Řešení:
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
### 1.2 Úkol
Vytvořte relace mezi tabulkami o zákazníkovi:
- Vytvořte relaci v `zakaznik`.
- Vytvořte cizí klíče pro tabulku `zakaznik_adresa` a `zakaznik_kontakt`.
````
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, MetaData, func, create_engine, inspect
from sqlalchemy.orm import relationship, declarative_base
````
Řešení:
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
Při vkládání dat do tabulky je důležité znát typy sloupců a jejich omezení.
	   
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
### 1.3 Úkol
Přidejte 5 záznamů do:
- `zakaznik`
- `zakaznik_kontakt`
- `zakaznik_adresa`

Řešení:
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
Nejčastější úlohou při práci s databází je vytažení údajů z nějaké tabulky -> <b>Select</b>
- V případě SQLAlchemy se využívá tato syntaxe:
````
session = Session()
result = session.query(Trida_tabulky).all()
session.commit()
````
Výpis pak provedme takto:
````
for row in result:
    print(row.sloupec1, row.sloupec2)
````
Filtrování v selectu se využívá pomocí <b>WHERE</b> podmínky.

V SQLAlchemy vypadá syntaxe takto:
````
session = Session()
result = session.query(Trida_tabulky).filter(Trida_tabulky.sloupec == hodnota).all()
session.commit()
````
Výpis pak provedme takto:
````
for row in result:
    print(row.sloupec1, row.sloupec2)
````
Důlěžitým prvkem může být také seřazení záznamů -> <b>Order By</b>
- V SQLAlchemy vypadá syntaxe takto:
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
Výpis pak provedme takto:
````
for row in result:
    print(row.sloupec1, row.sloupec2)
````
### 1.4 Úkol
Vytvořte z tabulky:
- `zakaznik` -> select, který vybere vše a vypíše jméno a příjmení 
- `zakaznik_adresa` -> select, který vybere pouze adresy trvalého bydliště a vypíše je
- `zakaznik_kontakt` -> select, který vybere vše a vypíše emaily seřazené sestupně

Řešení:
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
Kontrola:
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
Někdy je potřeba nějaké záznamy smazat.
- V SQLAlchemy vypadá syntaxe takto:
````
session = Session()
session.query(Trida_tabulky).filter(Trida_tabulky.sloupec == hodnota).delete()
session.commit()
````
### 1.5 Úkol
Smažte z tabulky `zakaznik_adresa` všechny adresy, které nejsou trvalé.

Řešení:
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
Kontrola:
````
session = Session()
result1 = session.query(ZakaznikAdress).all()
session.commit()

for zakaznik in result1:
    print(zakaznik.mesto, zakaznik.ulice)
print()
````
### Aktualizace hodnot
Pro některé úkony je třeba aktualizovat hodnoty.
- Slouží pro to syntaxe:

````
session = Session()
session.query(Trida_tabulky).filter(Trida_tabulky.sloupec == 'hodnota').update({"měněný sloupec": 'Nová hodnota'})
session.commit()
````
### 1.6 Úkol
Upravte sloupec `ulice` v tabulce `zakaznik_adresa`:
- Pokud je město **Cityville** -> ulice bude '``Nová ulice``'

Řešení:
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
Kontrola:
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
Naše databáze, kterou budeme používat, je velice jednoduchou simulací bankovního prostředí pro úvěry.
### ERD
![alt text](https://github.com/Hamzic12/SQL-Alchemy/blob/main/ERD.png)
### Tabulky
#### <b>CUSTOMER</b>
Tabulka klientů a jejich základní informace:
- <i>customer_id</i> = Identifikátor klienta
- <i>name</i> = Jméno klienta
- <i>surname</i> = Příjmení klienta
- <i>active_flag</i> = Označení zda je klient aktivní
#### <b>CUSTOMER_ADDRESS</b>
Tabulka adres klientů</i>:
- <i>customer_address_id</i> = Identifikátor adresy
- <i>psc</i> = PSČ 
- <i>city</i> = Město
- <i>street</i> = Ulice
- <i>number</i> = Číslo domu
- <i>domicile_flag</i> = Označení zda je to adresa trvalého bydliště
- <i>customer_id</i> = Idenfitikátor klienta
#### <b>CUSTOMER_CONTACT</b>
Tabulka kontaktů na klienty:
- <i>customer_contact_id</i> = Idenfitifkátor kontaktu
- <i>phone</i> = Telefonní číslo
- <i>email</i> = Email
- <i>customer_id</i> = Identifikátor klienta
#### <b>ACCOUNT</b>
Tabulka účtů a informace o nich:
- <i>account_id</i> = Identifikátor účtu
- <i>acc_type</i> = Typ účtu
- <i>acc_balance</i> = Zůstatek
- <i>active_flag</i> = Označení zda je účet aktivní
- <i>customer_id</i> = Identifikátor klienta
#### <b>BANK_USER</b>
Tabulka zaměsntanců a jejich základní informace:
- <i>bank_user_id</i> = Identifikátor zaměstnance
- <i>name</i> = Jméno zaměstnance
- <i>surname</i> = Příjmení zaměstnance
- <i>active_flag</i> = Označení zda je zaměstnanec aktivní
#### <b>BANK_USER_ADDRESS</b>
Tabulka adres zaměstnanců:
- <i>bank_user_adr_id</i> = Identifikátor adresy 
- <i>psc</i> = PSČ
- <i>city</i> = Město
- <i>street</i> = Ulice
- <i>number</i> = Číslo domu
- <i>domicile_flag</i> = Označení zda je to adresa trvalého bydliště
- <i>bank_user_id</i> = Identifikátor zaměstnance
#### <b>BANK_USER_CONTACT</b>
Tabulka kontaktů na zaměstnance:
- <i>bank_user_contact_id</i> = Identifikátor kontaktu
- <i>phone_work</i> = Pracovní telefonní číslo
- <i>email_work</i> = Pracovní email
- <i>phone_personal</i> = Osobní telefonní číslo
- <i>email_personal</i> = Osobní email
- <i>bank_user_id</i> = Identifikátor zaměstnance
#### <b>LOAN_UNPAYED</b>
Tabulka aktivních úvěrů a jejich informace:
- <i>loan_id</i> = Identifikátor úvěru
- <i>loan_type</i> = Typ úvěru
- <i>rem_instalment</i> = Zbývající počet splátek
- <i>instalment</i> = Celková výše úvěru
- <i>month_instalment</i> = Měsíční výše splátky
- <i>account_id</i> = Identifikátor účtu
- <i>bank_user_id</i> = Identifikátor zaměstnance, který úvěr sjednal
#### <b>LOAN_PAYED</b>
Tabulka splacených úverů:
- <i>loan_hist_id</i> = Identifikace splaceného úvěru
- <i>loan_type</i> = Typ úvěru
- <i>instalment</i> = Výše úvěru
- <i>account_id</i> = Identifikátor účtu

#### Toto si nahrajte do VSC:
````
from sqlalchemy import Column, Integer, String, Enum, MetaData, func, create_engine, inspect, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

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


engine = create_engine('sqlite:///:memory:', echo=False)

# Vytvoření schématu (metadata) pro tabulky
metadata = MetaData()

# Vytvoření tabulek
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

    # Vložení dat do tabulky CUSTOMER
session.add_all([
        Customer(name='John', surname='Doe', active_flag='Y'),
        Customer(name='Alice', surname='Smith', active_flag='Y'),
        Customer(name='Bob', surname='Johnson', active_flag='N'),
        Customer(name='Eva', surname='Nováková', active_flag='Y'),
        Customer(name='Martin', surname='Svoboda', active_flag='N'),
    ])

session.commit()

    # Vložení dat do tabulky ACCOUNT
session.add_all([
        Account(acc_type='STANDARD', account_number=1234, acc_balance=5000, active_flag='Y', customer_id=1),
        Account(acc_type='PLUS', account_number=5678, acc_balance=8000, active_flag='N', customer_id=2),
        Account(acc_type='STANDARD', account_number=9876, acc_balance=3000, active_flag='Y', customer_id=3),
        Account(acc_type='PLUS', account_number=5432, acc_balance=6000, active_flag='N', customer_id=4),
        Account(acc_type='STANDARD', account_number=6543, acc_balance=7000, active_flag='Y', customer_id=5),
    ])

session.commit()

    # Vložení dat do tabulky BANK_USER
session.add_all([
        BankUser(name='Adam', surname='White', active_flag='Y'),
        BankUser(name='Sophie', surname='Brown', active_flag='Y'),
        BankUser(name='Jack', surname='Miller', active_flag='N'),
        BankUser(name='Linda', surname='Anderson', active_flag='Y'),
        BankUser(name='Michael', surname='Young', active_flag='N'),
    ])

session.commit()

# Vložení dat do tabulky LOAN_UNPAYED
session.add_all([
        LoanUnpayed(loan_type='AUTO', rem_instalment=24, instalment=4000, month_instalment=200, account_id=1, bank_user_id=1),
        LoanUnpayed(loan_type='HYPO', rem_instalment=36, instalment=8000, month_instalment=300, account_id=2, bank_user_id=2),
        LoanUnpayed(loan_type='INVEST', rem_instalment=12, instalment=3000, month_instalment=250, account_id=3, bank_user_id=3),
        LoanUnpayed(loan_type='AUTO', rem_instalment=18, instalment=6000, month_instalment=350, account_id=4, bank_user_id=4),
        LoanUnpayed(loan_type='HYPO', rem_instalment=30, instalment=7000, month_instalment=400, account_id=5, bank_user_id=5),
    ])

session.commit()

    # Vložení dat do tabulky BANK_USER_CONTACT
session.add_all([
        BankUserContact(phone_work='123-456-7890', email_work='adam.white@example.com', phone_personal='987-654-3210', email_personal='adam.personal@example.com', bank_user_id=1),
        BankUserContact(phone_work='234-567-8901', email_work='sophie.brown@example.com', phone_personal='876-543-2109', email_personal='sophie.personal@example.com', bank_user_id=2),
        BankUserContact(phone_work='345-678-9012', email_work='jack.miller@example.com', phone_personal='765-432-1098', email_personal='jack.personal@example.com', bank_user_id=3),
        BankUserContact(phone_work='456-789-0123', email_work='linda.anderson@example.com', phone_personal='654-321-0987', email_personal='linda.personal@example.com', bank_user_id=4),
        BankUserContact(phone_work='567-890-1234', email_work='michael.young@example.com', phone_personal='543-210-9876', email_personal='michael.personal@example.com', bank_user_id=5),
    ])

session.commit()

    # Vložení dat do tabulky BANK_USER_ADDRESS
session.add_all([
        BankUserAddress(psc='12345', city='New York', street='Broadway', number='42', domicile_flag='Y', bank_user_id=1),
        BankUserAddress(psc='54321', city='Los Angeles', street='Hollywood Blvd', number='7', domicile_flag='N', bank_user_id=2),
        BankUserAddress(psc='67890', city='Chicago', street='Michigan Ave', number='15', domicile_flag='Y', bank_user_id=3),
        BankUserAddress(psc='98765', city='San Francisco', street='Market St', number='20', domicile_flag='N', bank_user_id=4),
        BankUserAddress(psc='87654', city='Miami', street='Ocean Dr', number='30', domicile_flag='Y', bank_user_id=5),
    ])

session.commit()

    # Vložení dat do tabulky CUSTOMER_ADDRESS
session.add_all([
        CustomerAddress(psc='12345', city='Prague', street='Main St', number='1', domicile_flag='Y', customer_id=1),
        CustomerAddress(psc='54321', city='Brno', street='Masaryk St', number='5', domicile_flag='N', customer_id=2),
        CustomerAddress(psc='67890', city='Ostrava', street='Long St', number='15', domicile_flag='Y', customer_id=3),
        CustomerAddress(psc='98765', city='Plzen', street='Square St', number='20', domicile_flag='N', customer_id=4),
        CustomerAddress(psc='87654', city='Liberec', street='Freedom St', number='30', domicile_flag='Y', customer_id=5),
    ])

session.commit()

    # Vložení dat do tabulky CUSTOMER_CONTACT
session.add_all([
        CustomerContact(phone='123-456-7890', email='john.doe@example.com', customer_id=1),
        CustomerContact(phone='234-567-8901', email='alice.smith@example.com', customer_id=2),
        CustomerContact(phone='345-678-9012', email='bob.johnson@example.com', customer_id=3),
        CustomerContact(phone='456-789-0123', email='eva.novakova@example.com', customer_id=4),
        CustomerContact(phone='567-890-1234', email='martin.svoboda@example.com', customer_id=5),
    ])

session.commit()

    # Vložení dat do tabulky LOAN_PAYED
session.add_all([
        LoanPayed(loan_type='AUTO', instalment=4000, account_id=1),
        LoanPayed(loan_type='HYPO', instalment=8000, account_id=2),
        LoanPayed(loan_type='INVEST', instalment=3000, account_id=3),
        LoanPayed(loan_type='AUTO', instalment=6000, account_id=4),
        LoanPayed(loan_type='HYPO', instalment=7000, account_id=5),
    ])

session.commit()

    # Uzavření Session
session.close()
    
inspector = inspect(engine)
    
table_names = inspector.get_table_names()
print(f"Seznam tabulek: {table_names}")
````

### Agregační funkce v SQLAlchemy
- <b>sum()</b>: Součet hodnot v daném sloupci.
- <b>avg()</b>: Průměr hodnot v daném sloupci.
- <b>count()</b>: Počet záznamů v dané tabulce.
- <b>min()</b>: Minimální hodnota v daném sloupci.
- <b>max()</b>: Maximální hodnota v daném sloupci.

Pro využití funkcí je potřeba importovat `func`:
````
from sqlalchemy import func
````

Příklad použití:
````
session = Session()
prumerny_plat = session.query(func.avg(Zamestnanec.plat)).scalar()
pocet_zamestnancu = session.query(func.count(Zamestnanec.id)).scalar()
session.commit()
````
Výpis výsledků:
````
print(f"Průměrný plat: {prumerny_plat}")
print(f"Počet zaměstnanců: {pocet_zamestnancu}")
````

Proč .scalar?
- Scalar se využívá pokud očekávám výstup o jedné hodnotě.
- Scalar nepoužijeme pokud chceme např. výběr všech sloupců z tabulky.

#### Group By
Agregační funkce se dají kombinovat s klauzulí GROUP BY, sloužící k seskupení dat a výpočet agregací pro každou skupinu:
````
session = Session()

# Výpočet průměrného platu pro každé oddělení
vysledky = session.query(Zamestnanec.oddeleni, func.avg(Zamestnanec.plat)).group_by(Zamestnanec.oddeleni).all()
session.commit()
````
Výpis výsledků:
````
for radek in vysledky:
    print(f"Oddělení: {radek.oddeleni}")
    print(f"Průměrný plat: {radek.avg_plat}")
````

#### Filtrování agregovaných hodnot

Agregované výsledky se dají dále filtrovat s WHERE(filter) klauzulí.

Výpočet průměrného platu pro zaměstnance s platem nad 50 000:
````
session = Session()

prumerny_plat = session.query(func.avg(Zamestnanec.plat)).filter(Zamestnanec.plat > 50000).scalar()
session.commit()
````
Výpis výsledku:
````
print(f"Průměrný plat pro zaměstnance s platem nad 50 000: {prumerny_plat}")
````
### 2.1 Úkol:
- Spočítat součet všech úvěrů (LoanUnpayed)
- Spočítat počet 'Hypo' úvěrů (LoanUnpayed)
- Najít minimální balanci z účtů (Accounts)
- Najít maximální balanci z účtů (Accounts)
- Spočítat průměrnou výši úvěru (LoanUnpayed)

Řešení:
````
soucet_uveru = session.query(func.sum(LoanUnpayed.instalment)).scalar()
pocet_hypo = session.query(func.count(LoanUnpayed.instalment)).filter(LoanUnpayed.loan_type == 'HYPO').scalar()
min_balance = session.query(func.min(Account.acc_balance)).scalar()
max_balance = session.query(func.max(Account.acc_balance)).scalar()
avg_uver = session.query(func.avg(LoanUnpayed.instalment)).scalar()
````
Výpis:
````
print(f"Celkový součet úverů je: {soucet_uveru}Kč")
print(f"Celkový počet HYPO úvěrů je: {pocet_hypo}")
print(f"Minimální balance je: {min_balance}Kč")
print(f"Maximální balance je: {max_balance}Kč")
print(f"Průměrná výše úvěru je: {avg_uver}Kč")
````

### Spojování tabulek
Spojování tabulek (JOIN) umožňuje kombinovat data z více tabulek v databázi do jediné tabulky.
- Dnes si vysvětlíme tři základní joiny.
````
from sqlalchemy import join
````
#### Inner Join
Vrátí záznamy, které existují v obou tabulkách.
````
session = Session()
vysledky = session.query(Osoba, Adresa).join(Adresa, Osoba.adresa_id == Adresa.id).all()
session.commit()
````
Výpis:
````
for osoba, adresa in vysledky:
    print(f"{osoba.jmeno} - {adresa.ulice}, {adresa.mesto}")
````
#### Left Join
Vrátí všechny záznamy z levé tabulky a odpovídající záznamy z pravé tabulky (i když v pravé tabulce neexistují).
````
session = Session()
vysledky = session.query(Osoba).outerjoin(Adresa, Osoba.adresa_id == Adresa.id).all()
session.commit()
````
Výpis:
````
for osoba in vysledky:
    if osoba.adresa:
        print(f"{osoba.jmeno} - {adresa.ulice}, {adresa.mesto}")
    else:
        print(f"{osoba.jmeno} - nemá adresu")
````
#### Right Join
Vrátí všechny záznamy z pravé tabulky a odpovídající záznamy z levé tabulky (i když v levé tabulce neexistují).
````
session = Session()
vysledky = session.query(Adresa).outerjoin(Osoba, Osoba.adresa_id == Adresa.id).all()
session.commit()
````
Výpis:
````
for adresa in vysledky:
    if adresa.osoba:
        print(f"{adresa.ulice}, {adresa.mesto} - {osoba.jmeno}")
    else:
        print(f"{adresa.ulice}, {adresa.mesto} - neobsazeno")
````

### 2.2 Úkol:
- Vytvořte všechny joiny, které jsme si zde představili nad tabulkami `Customer` a `CustomerAdress`.

Řešení:
````
vysledky_inner = session.query(Customer, CustomerAddress).join(CustomerAddress, Customer.customer_id == CustomerAddress.customer_id).all()
vysledky_left = session.query(Customer).outerjoin(CustomerAddress, Customer.customer_id == CustomerAddress.customer_id).all()
vysledky_right = session.query(CustomerAddress).outerjoin(Customer, Customer.customer_id == CustomerAddress.customer_id).all()
````
Výpis:
````
for zakaznik, adresa in vysledky_inner:
    print(f"{zakaznik.name} - {adresa.street}, {adresa.city}")
    
print()

for zakaznik in vysledky_left:
    adresy = zakaznik.addresses

    if adresy:
        for adresa in adresy:
            print(f"{zakaznik.name} - {adresa.street}, {adresa.city}")
    else:
        print(f"{zakaznik.name} - nemá adresu")
        
print()

for kontakt in vysledky_right:
    zakaznik = kontakt.customer
    kontakty = zakaznik.contacts

    if kontakty:
        for k in kontakty:
            print(f"{zakaznik.name} - {k.email}, {k.phone}")
    else:
        print(f"{zakaznik.name} - nemá kontakt")
````

### Vytvoření cache
Pro lepší výkonnost je možné využívat cachce - malá ale velice rychlá paměť.
````
from werkzeug.utils import cached_property
````
````
class Osoba(Base):
    ...

    @cached_property
    def plne_jmeno(self):
        return f"{self.jmeno} {self.prijmeni}"

session = Session()

osoba = session.query(Osoba).filter(Osoba.id == 1).first()
session.close()
````
Výpis:
````
print(osoba.plne_jmeno)
````
### 2.3 Úkol:
- Vytvořte pro tabulku `Customer` cache pro jméno a příjmení.

Řešení:
````
class Customer(Base):
    __tablename__ = 'customer'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    surname = Column(String(46), nullable=False)
    active_flag = Column(Enum('Y', 'N'), nullable=False, default='Y', server_default='Y')
    
    __table_args__ = (
        UniqueConstraint('customer_id', name='customer_id_UNIQUE'),
    )
    @cached_property
    def full_name(self):
        return f"{self.name} {self.surname}"
````
Výpis:
````
zakaznik = session.query(Customer).filter(Customer.customer_id == 1).first()
print(zakaznik.full_name)
````
## 3. Část
````
from sqlalchemy import Column, Integer, String, Enum, MetaData, func, create_engine, inspect, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

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


engine = create_engine('sqlite:///:memory:', echo=False)

# Vytvoření schématu (metadata) pro tabulky
metadata = MetaData()

# Vytvoření tabulek
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

    # Vložení dat do tabulky CUSTOMER
session.add_all([
        Customer(name='John', surname='Doe', active_flag='Y'),
        Customer(name='Alice', surname='Smith', active_flag='Y'),
        Customer(name='Bob', surname='Johnson', active_flag='N'),
        Customer(name='Eva', surname='Nováková', active_flag='Y'),
        Customer(name='Martin', surname='Svoboda', active_flag='N'),
    ])

session.commit()

    # Vložení dat do tabulky ACCOUNT
session.add_all([
        Account(acc_type='STANDARD', account_number=1234, acc_balance=5000, active_flag='Y', customer_id=1),
        Account(acc_type='PLUS', account_number=5678, acc_balance=8000, active_flag='N', customer_id=2),
        Account(acc_type='STANDARD', account_number=9876, acc_balance=3000, active_flag='Y', customer_id=3),
        Account(acc_type='PLUS', account_number=5432, acc_balance=6000, active_flag='N', customer_id=4),
        Account(acc_type='STANDARD', account_number=6543, acc_balance=7000, active_flag='Y', customer_id=5),
    ])

session.commit()

    # Vložení dat do tabulky BANK_USER
session.add_all([
        BankUser(name='Adam', surname='White', active_flag='Y'),
        BankUser(name='Sophie', surname='Brown', active_flag='Y'),
        BankUser(name='Jack', surname='Miller', active_flag='N'),
        BankUser(name='Linda', surname='Anderson', active_flag='Y'),
        BankUser(name='Michael', surname='Young', active_flag='N'),
    ])

session.commit()

# Vložení dat do tabulky LOAN_UNPAYED
session.add_all([
        LoanUnpayed(loan_type='AUTO', rem_instalment=24, instalment=4000, month_instalment=200, account_id=1, bank_user_id=1),
        LoanUnpayed(loan_type='HYPO', rem_instalment=36, instalment=8000, month_instalment=300, account_id=2, bank_user_id=2),
        LoanUnpayed(loan_type='INVEST', rem_instalment=12, instalment=3000, month_instalment=250, account_id=3, bank_user_id=3),
        LoanUnpayed(loan_type='AUTO', rem_instalment=18, instalment=6000, month_instalment=350, account_id=4, bank_user_id=4),
        LoanUnpayed(loan_type='HYPO', rem_instalment=30, instalment=7000, month_instalment=400, account_id=5, bank_user_id=5),
    ])

session.commit()

    # Vložení dat do tabulky BANK_USER_CONTACT
session.add_all([
        BankUserContact(phone_work='123-456-7890', email_work='adam.white@example.com', phone_personal='987-654-3210', email_personal='adam.personal@example.com', bank_user_id=1),
        BankUserContact(phone_work='234-567-8901', email_work='sophie.brown@example.com', phone_personal='876-543-2109', email_personal='sophie.personal@example.com', bank_user_id=2),
        BankUserContact(phone_work='345-678-9012', email_work='jack.miller@example.com', phone_personal='765-432-1098', email_personal='jack.personal@example.com', bank_user_id=3),
        BankUserContact(phone_work='456-789-0123', email_work='linda.anderson@example.com', phone_personal='654-321-0987', email_personal='linda.personal@example.com', bank_user_id=4),
        BankUserContact(phone_work='567-890-1234', email_work='michael.young@example.com', phone_personal='543-210-9876', email_personal='michael.personal@example.com', bank_user_id=5),
    ])

session.commit()

    # Vložení dat do tabulky BANK_USER_ADDRESS
session.add_all([
        BankUserAddress(psc='12345', city='New York', street='Broadway', number='42', domicile_flag='Y', bank_user_id=1),
        BankUserAddress(psc='54321', city='Los Angeles', street='Hollywood Blvd', number='7', domicile_flag='N', bank_user_id=2),
        BankUserAddress(psc='67890', city='Chicago', street='Michigan Ave', number='15', domicile_flag='Y', bank_user_id=3),
        BankUserAddress(psc='98765', city='San Francisco', street='Market St', number='20', domicile_flag='N', bank_user_id=4),
        BankUserAddress(psc='87654', city='Miami', street='Ocean Dr', number='30', domicile_flag='Y', bank_user_id=5),
    ])

session.commit()

    # Vložení dat do tabulky CUSTOMER_ADDRESS
session.add_all([
        CustomerAddress(psc='12345', city='Prague', street='Main St', number='1', domicile_flag='Y', customer_id=1),
        CustomerAddress(psc='54321', city='Brno', street='Masaryk St', number='5', domicile_flag='N', customer_id=2),
        CustomerAddress(psc='67890', city='Ostrava', street='Long St', number='15', domicile_flag='Y', customer_id=3),
        CustomerAddress(psc='98765', city='Plzen', street='Square St', number='20', domicile_flag='N', customer_id=4),
        CustomerAddress(psc='87654', city='Liberec', street='Freedom St', number='30', domicile_flag='Y', customer_id=5),
    ])

session.commit()

    # Vložení dat do tabulky CUSTOMER_CONTACT
session.add_all([
        CustomerContact(phone='123-456-7890', email='john.doe@example.com', customer_id=1),
        CustomerContact(phone='234-567-8901', email='alice.smith@example.com', customer_id=2),
        CustomerContact(phone='345-678-9012', email='bob.johnson@example.com', customer_id=3),
        CustomerContact(phone='456-789-0123', email='eva.novakova@example.com', customer_id=4),
        CustomerContact(phone='567-890-1234', email='martin.svoboda@example.com', customer_id=5),
    ])

session.commit()

    # Vložení dat do tabulky LOAN_PAYED
session.add_all([
        LoanPayed(loan_type='AUTO', instalment=4000, account_id=1),
        LoanPayed(loan_type='HYPO', instalment=8000, account_id=2),
        LoanPayed(loan_type='INVEST', instalment=3000, account_id=3),
        LoanPayed(loan_type='AUTO', instalment=6000, account_id=4),
        LoanPayed(loan_type='HYPO', instalment=7000, account_id=5),
    ])

session.commit()

    # Uzavření Session
session.close()
````
### 1. Dotazy a analýzy:
- Vypište všechny zákazníky a jejich zůstatky na účtech.
- Vypočítejte celkový zůstatek na všech účtech.
- Vyhledejte nezaplacené půjčky a připojte k nim jména zákazníků.
- Sestavte přehled počtu zákazníků a bankovních uživatelů v jednotlivých městech.

### 2. Úpravy a aktualizace:
- Přidejte nového zákazníka s účtem a kontaktními údaji.
- Změňte adresu jednoho z bankovních uživatelů.
- Aktualizujte stav půjčky z "Nezaplaceno" na "Splaceno" (Y/N).
- Deaktivujte účet zákazníka, který si přeje ukončit spolupráci.

### 3. Experimenty s funkcionalitami:
- Vytvořte příkaz, který zobrazí detailní informace o konkrétním účtu.
- Vytvořte příkaz pro vyhledávání zákazníků podle jména nebo příjmení.
- Vytvořte report, který zobrazí přehled zůstatků na účtech seřazený sestupně.
- Vytvořte příkaz pro simulaci výběru hotovosti z účtu.

### 4. Opravy a kontroly:
- Vyhledejte a opravte chybné nebo nekonzistentní údaje v databázi (např. neodpovídající sumy).
