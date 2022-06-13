# kaffeDatabase

con = sqlite3.connect("kaffe.sql")


## Hvordan man connecter og skriver spørringer til db

cursor = con.cursor()

cursor.execute(" Skriv inn spørringen din her") feks Select * from navn

con.close() greit å lukke den når den er ferdig

Hvordan skrive 'pen' spørring

cursor.execute("SELECT * FROM person WHERE navn = ?", [navn])


# Man henter ut ved hjelp av fetch(one/all/many):

cursor.execute("Select * form PERSON")

row = cursor.fetchone()

print("First row from table person:")

rows = cursor.fetchall()

print("All rows in the table person:")

rows = cursor.fetchmany(2)

print("First two rows from table person:")

eller så kan man bruke en for-løkke (for row in "spørring": do this do that)

# Skrive til database 

cursor.execute('''CREATE TABLE person

(id INTEGER PRIMARY KEY, name TEXT, birthday TEXT)''')

cursor.execute('''INSERT INTO person VALUES (1, 'Ola Nordmann', '2002-02-02')''')

connection.commit()

connection.close()
