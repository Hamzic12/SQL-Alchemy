# SQL-Alchemy
## Úvod do SQLAlchemy
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
