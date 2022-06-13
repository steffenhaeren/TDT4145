from datetime import datetime
import os.path
import sqlite3


# Alt skrives på norsk


def ranger(epost):
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "kaffedb.db")
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    cursor.execute("select Count(*) from Kaffesmaking")
    (smaksID, ) = cursor.fetchone()
    smaksID = int(smaksID)
    smaksID+=1

    cursor.execute(f"select Bruker.BrukerID from Bruker where Bruker.Epost = '{epost}'")
    (id, ) = cursor.fetchone()
    id = int(id)
    kaffenavn = input("Hva het kaffen?")
    
    try:
        cursor.execute(f"select Kaffe.KaffeID from Kaffe where Kaffe.KaffeNavn = '{kaffenavn}'")
        (kaffeid, ) = cursor.fetchone()
        kaffeid = str(kaffeid)
    except:
        print("Something went wrong")

    datoen = datetime.today().strftime('%Y-%m-%d')

    poeng = int(input("Hvor mange poeng vil du gi den?"))
    notat = str(input("Skriv notater her: "))
    try: 
        # her legges in dagens dato fra smaking (sto i kunngjøring at dette er greit)
        cursor.execute(f"INSERT INTO Kaffesmaking VALUES ('{smaksID}', '{id}', '{notat}', '{poeng}', '{datoen}', '{kaffeid}')")
        con.commit()
        print("Du fikk lagt til en smaking\n\n")
    except: 
        print("Something did not work\n\n")
    cursor.close()

# Skal være ferdig nå
def sok_brukere():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "kaffedb.db")
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    try:
        cursor.execute("""select Bruker.Navn, COUNT(DISTINCT Kaffesmaking.KaffeID) as dist from Bruker natural join Kaffesmaking where Kaffesmaking.dato > 2021 GROUP BY Bruker.BrukerID ORDER BY dist desc""")
        for row in cursor.fetchall():
            print("Navn: " + str(row[0]) + "\nKaffesmakinger: " + str(row[1]))
    
    except:
        print("Det finnes ingen kaffesmakinger i år")
    cursor.close()


def se_beste_kaffer():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "kaffedb.db")
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    try: 
        cursor.execute("""SELECT BrenneriNavn, KaffeNavn, avg(Kaffesmaking.Poeng) as Score, Kaffe.Kilopris from Kaffesmaking join Kaffe on (Kaffesmaking.KaffeID = Kaffe.KaffeID) join Kaffebrenneri on (Kaffebrenneri.BrenneriID = Kaffe.BrenneriID) GROUP BY Kaffe.KaffeID ORDER BY Kaffesmaking.Poeng DESC""")
        for row in cursor.fetchall():
            print("Brennerinavn: " + str(row[0]) + "\nKaffenavn: " + str(row[1]) + "\nAvg Score: " + str(row[2]) + "\nPris: " + str(row[3]))
    except: 
        print("Noe gikk galt")

    cursor.close()

def sok_med_stikkord():

    sokeord = input("Hvilket ord vil du søke etter?")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "kaffedb.db")
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    # Hvis man søker etter deler av ordet vil det også gå, men det er forsåvet greit
    try:
        cursor.execute(f"SELECT KaffeNavn FROM Kaffe JOIN Kaffesmaking ON (Kaffe.KaffeId = Kaffesmaking.KaffeID) WHERE Kaffesmaking.Beskrivelse LIKE '%{sokeord}%'")
        for row in cursor.fetchall(): 
            print("Kaffenavn: " + str(row[0]))
    except: 
        print("Fant ingen Brukere har beskrevet en kaffen slik\n")
    try: 
        cursor.execute(f"""SELECT BrenneriNavn from Kaffe join Kaffebrenneri ON (Kaffe.BrenneriID = Kaffebrenneri.BrenneriID) WHERE Kaffe.Beskrivelse LIKE '%{sokeord}%'""")
        for row in cursor.fetchall(): 
            print("Brennerinavn: " + str(row[0]))
    except: 
        print("Fant ingen Brennerier har beskrevet en kaffen slik\n")
    cursor.close()

def sok_etter_foredling():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "kaffedb.db")
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    foredlingsmetode = input("Hvilken foredlingsmetode ønsker du å filtrere etter?")
    land = input("Hvilket land vil du søke etter?\n")

    
    try: 
        cursor.execute(f"select KaffeNavn, BrenneriNavn from Kaffe join Kaffebrenneri on (Kaffe.BrenneriID = Kaffebrenneri.BrenneriID) join Kaffeparti on (Kaffeparti.PartiID = Kaffe.PartiID) join Kaffegaard on (Kaffeparti.GaardsID = Kaffegaard.GaardsID) join Foredling on (Kaffeparti.ForedlingID = Foredling.ForedlingID) where (Foredling.Fordelingsmetode like '%{foredlingsmetode}%' AND Kaffegaard.Land like '%{land}%')")
        for row in cursor.fetchall():
            print("Kaffenavn: " + row[0] + "\nGårdsnavn: " + row[1] + "\n\n" )
    except:
        print("Det finnes ingen kaffer basert på det")
    cursor.close()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "kaffedb.db")
con = sqlite3.connect(db_path)
cursor = con.cursor()

# Her vil main-funksjonen vår kjøre fra
print("Hei, velkommen til SETkaffe\u2122\n")
print("Vennligst logg inn:\n")

# Evig løkke til vi kjører "break"
valg = 0
while valg != 6:

    epost = input("Epost: ")
    passord = input("Passord: ")

    cursor.execute("SELECT BrukerID FROM Bruker WHERE Epost = ?", [epost])
    (brukerID, ) = cursor.fetchone()
    #Legge til fielmelding hvis bruker ikke finnes i systemet
    
    cursor.execute("SELECT Passord FROM Bruker WHERE BrukerID = ?", [brukerID])
    (bruker_passord, ) = cursor.fetchone()

    if (bruker_passord == passord): 
        print("Du har logget inn :)")
        print("Hva vil du gjøre?")
        while True: 
            # Akk nå vil denne runne for evig
            print("1: Ranger en kaffe\n2: Se brukere med flest unike kaffer i år\n3: Se hvilke kaffer som gir mest for penga")
            print("4: Søk med stikkord\n5: Søk etter foredlingsmetoder brukt/ikke brukt fra forskjellige land")
            print("6: For å avslutte ")

            valg = input("")
            try:
                valg = int(valg)
                if (valg == 1):
                    ranger(epost)
                    continue
                elif (valg == 2):
                    sok_brukere()
                    continue
                elif(valg == 3):
                    se_beste_kaffer()
                    continue
                elif (valg == 4):
                    sok_med_stikkord()
                    continue
                elif (valg == 5):
                    sok_etter_foredling()
                    continue
                elif (valg == 6):
                    print("Ha det bra :)")
                    break
                else:
                    print("Feil input, prøv igjen")
                    continue
            except:
                print("Feil i input, prøv igjen")
                continue

    else: 
        print("Noe gikk feil")
        print("Vil du prøve igjen? y/n")
        if (input(": ") == "y"): 
            continue
        else:
            print("Ha det bra :)")
            break




