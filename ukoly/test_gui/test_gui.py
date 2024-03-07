# použijeme knihovnu tkinter
import tkinter as tk

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# vytvoříme novou třídu z base (abstraktní základní třída pro všechny tabulky)
Base = declarative_base()

# a vytvoříme tabulku, jak jsme si ukázali
class Zakaznik(Base):
    __tablename__ = 'zakaznik'
    
    id_zak = Column(Integer, primary_key=True, autoincrement=True)
    jmeno = Column(String(25))
    prijmeni = Column(String(25))
    dt_create = Column(DateTime, server_default=func.now())

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)  

Session = sessionmaker(bind=engine)
session = Session()



# přidání zákazníka
def add_zakaznik():
    jmeno = entry_jmeno.get() # get() je metoda Entry widgetu pro načtení hodnoty do proměnné
    prijmeni = entry_prijmeni.get()
    zakaznik = Zakaznik(jmeno=jmeno, prijmeni=prijmeni) # vytvoření instance objektu Zakaznik s předanými parametry
    session.add(zakaznik)
    session.commit()
    display_zakaznik()

# zobrazení přidaných dat
def display_zakaznik():
    for widget in frame_display.winfo_children():
        widget.destroy()
    zakaznici = session.query(Zakaznik).all()
    for i, zakaznik in enumerate(zakaznici):
        label = tk.Label(frame_display, text=f"{zakaznik.id_zak} | {zakaznik.jmeno} {zakaznik.prijmeni} | {zakaznik.dt_create}")
        label.grid(row=i, column=0, padx=5, pady=5)

    # jednoduchý výpis od konzole
    for zakaznik in zakaznici:
        print(f"ID: {zakaznik.id_zak}, Jméno: {zakaznik.jmeno}, Příjmení: {zakaznik.prijmeni}, Datum vytvoření: {zakaznik.dt_create}")

root = tk.Tk()
root.title("Zakaznik GUI") # nadpis okna

# odsazení
frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10)

# label + vstupní pole pro jméno
label_jmeno = tk.Label(frame_input, text="Jméno:")
label_jmeno.grid(row=0, column=0, padx=5, pady=5)
entry_jmeno = tk.Entry(frame_input)
entry_jmeno.grid(row=0, column=1, padx=5, pady=5)

# label + vstupní pole pro příjmení
label_prijmeni = tk.Label(frame_input, text="Příjmení:")
label_prijmeni.grid(row=1, column=0, padx=5, pady=5)
entry_prijmeni = tk.Entry(frame_input)
entry_prijmeni.grid(row=1, column=1, padx=5, pady=5)

# tlačítko pro přidání dat
button_add = tk.Button(frame_input, text="Přidat", command=add_zakaznik)
button_add.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

frame_display = tk.Frame(root)
frame_display.pack(padx=10, pady=10)

display_zakaznik()

# běh okna
root.mainloop()
