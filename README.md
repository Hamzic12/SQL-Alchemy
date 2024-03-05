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
1) Tvorba databáze
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
	vztah = relationship("second_table")
	
class SecondTable(Base):
    __tablename__ = 'second_table'
    id = Column(Integer, primary_key=True)
    first_table_id = Column(Integer, ForeignKey('first_table.id'))
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
