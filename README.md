# SQL-Alchemy
## Úvod do SQLAlchemy
### Databáze
Naše databáze, kterou budeme používat, je velice jednoduchou simulací bankovního prostředí pro úvěry
### ERD
![alt text](https://github.com/Hamzic12/SQL-Alchemy/blob/main/ERD.png)
### Tabulky
#### <b>CUSTOMER</b>
Tabulka klientů a jejich základní informace
- <i>customer_id</i>
- <i>name</i>
- <i>surname</i>
- <i>active_flag</i>
#### <b>CUSTOMER_ADDRESS</b>
Tabulka adres klientů</i>
- <i>customer_address_id</i>
- <i>psc</i>
- <i>city</i>
- <i>street</i>
- <i>number</i>
- <i>domicile_flag</i>
- <i>customer_id</i>
#### <b>CUSTOMER_CONTACT</b>
Tabulka kontaktů na klienty
- <i>customer_contact_id</i>
- <i>phone</i>
- <i>email</i>
- <i>customer_id</i>
#### <b>ACCOUNT</b>
Tabulka účtů a informace o nich
- <i>account_id</i>
- <i>acc_type</i>
- <i>acc_balance</i>
- <i>active_flag</i>
- <i>customer_id</i>
#### <b>BANK_USER</b>
Tabulka zaměsntanců a jejich základní informace
- <i>bank_user_id</i>
- <i>name</i>
- <i>surname</i>
- <i>active_flag</i>
#### <b>BANK_USER_ADDRESS</b>
Tabulka adres zaměstnanců 
- <i>bank_user_adr_id</i>
- <i>psc</i>
- <i>city</i>
- <i>street</i>
- <i>number</i>
- <i>domicile_flag</i>
- <i>bank_user_id</i>
#### <b>BANK_USER_CONTACT</b>
Tabulka kontaktů na zaměstnance
- <i>bank_user_contact_id</i>
- <i>phone_work</i>
- <i>email_work</i>
- <i>phone_personal</i>
- <i>email_personal</i>
- <i>bank_user_id</i>
#### <b>LOAN_UNPAYED</b>
Tabulka aktivních úvěrů a jejich informace
- <i>loan_id</i>
- <i>loan_type</i>
- <i>rem_instalment</i>
- <i>instalment</i>
- <i>month_instalment</i>
- <i>account_id</i>
- <i>bank_user_id</i>
#### <b>LOAN_PAYED</b>
Tabulka splacených úverů
- <i>loan_hist_id</i>
- <i>loan_type</i>
- <i>instalment</i>
- <i>account_id</i>
