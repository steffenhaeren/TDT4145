CREATE TABLE Bruker (
    BrukerID   INTEGER NOT NULL,
    Epost      VARCHAR(50) NOT NULL,
    Navn       VARCHAR(30) NOT NULL,
    Passord    VARCHAR(30) NOT NULL,
    CONSTRAINT Bruker_PK PRIMARY KEY (BrukerID)
  );
  
  
CREATE TABLE Kaffegaard(
    GaardsID       INTEGER NOT NULL,
    GaardsNavn     VARCHAR(30) NOT NULL,
    Land          VARCHAR(30) NOT NULL,
    Region        VARCHAR(30) NOT NULL,
    Moh           INTEGER NOT NULL,
    CONSTRAINT Kaffegaard_PK PRIMARY KEY (GaardsID),
);
 CREATE TABLE Kaffeboenne(
    BoenneID      INTEGER NOT NULL,
    Artsnavn     VARCHAR(30) NOT NULL,
    CONSTRAINT Kaffeboenne_PK PRIMARY KEY (BoenneID)
);


CREATE TABLE  Kaffeparti (
    PartiID         INTEGER NOT NULL,
    Innhoestingsaar   INTEGER NOT NULL,
    Kilopris        INTEGER NOT NULL,
    GaardsID         INTEGER NOT NULL,
    ForedlingID     INTEGER NOT NULL,
    CONSTRAINT Kaffeparti_PK PRIMARY KEY (PartiID),
    CONSTRAINT Kaffeparti_FK1 FOREIGN KEY (ForedlingID) REFERENCES Foredling(ForedlingID)
      ON UPDATE CASCADE
      ON DELETE CASCADE,
    CONSTRAINT Kaffeparti_FK2 FOREIGN KEY (GaardsID) REFERENCES Kaffegaard(GaardsID)
      ON UPDATE CASCADE
      ON DELETE CASCADE);

CREATE TABLE Foredling(
    ForedlingID         INTEGER NOT NULL,
    Fordelingsmetode    VARCHAR(30) NOT NULL,
    Beskrivelse         VARCHAR(100),
    CONSTRAINT Foredling_PK PRIMARY KEY (ForedlingID)
);



CREATE TABLE Kaffe (
  KaffeID         INTEGER NOT NULL,
  KaffeNavn       VARCHAR(30) NOT NULL,
  Navn            VARCHAR(30) NOT NULL,
  Beskrivelse     VARCHAR(100),
  Brenningsgrad   VARCHAR(10) CHECK (Brenningsgrad = 'lys' OR Brenningsgrad = 'middels' OR Brenningsgrad = 'moerk'),
  BrenningDato    DATE NOT NULL,
  Kilopris        INTEGER NOT NULL,
  BrenneriID      INTEGER NOT NULL,
  PartiID         INTEGER NOT NULL,
  CONSTRAINT Kaffe_PK PRIMARY KEY (KaffeID),
  CONSTRAINT Kaffe_FK1 FOREIGN KEY (BrenneriID) REFERENCES Kaffebrenneri(BrenneriID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT Kaffe_FK2 FOREIGN KEY (PartiID) REFERENCES Kaffeparti(PartiID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
  );



CREATE TABLE Kaffesmaking (
  SmakID         INTEGER NOT NULL,
  BrukerID       VARCHAR(30) NOT NULL,
  Beskrivelse    VARCHAR(100),
  Poeng          INTEGER CHECK (Poeng >= 0 AND Poeng <= 10),
  Dato           DATE NOT NULL,
  KaffeID        INTEGER NOT NULL,
  CONSTRAINT Kaffesmaking_PK PRIMARY KEY (SmakID),
  CONSTRAINT Kaffesmaking_FK1 FOREIGN KEY (BrukerID) REFERENCES Bruker(BrukerID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT Kaffesmaking_FK2 FOREIGN KEY (KaffeID) REFERENCES Kaffe(KaffeID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE Boenneparti(
    BoenneID    INTEGER NOT NULL,
    PartiID    INTEGER NOT NULL,
	CONSTRAINT Boenneparti_FK1 FOREIGN KEY (PartiID) REFERENCES Kaffeparti(PartiID)
  ON UPDATE CASCADE
	ON DELETE CASCADE,
	CONSTRAINT Boenneparti_FK2 FOREIGN KEY (BoenneID) REFERENCES Kaffeboenne(BoenneID)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

CREATE TABLE Kaffebrenneri(
    BrenneriID        INTEGER NOT NULL,
    BrenneriNavn      VARCHAR(30) NOT NULL,
    CONSTRAINT Kaffebrenneri_PK PRIMARY KEY (BrenneriID)
  );