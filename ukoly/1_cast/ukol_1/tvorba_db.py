from sqlalchemy import Column, Integer, String, DateTime, Enum, MetaData, func, create_engine, inspect
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

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
        columns = inspector.get_columns(table_name)

    # Vytisknutí informací o sloupcích
        print()
        print(f"Struktura tabulky '{table_name}':")
        for column in columns:
            print(f"Název sloupce: {column['name']}, Typ sloupce: {column['type']}")
        print()


# Spuštění funkce
create_tables()