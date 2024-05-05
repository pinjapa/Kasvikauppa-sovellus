# Kasvikauppa-sovellus

Sovelluksen toiminnallisuus:

- Sovellukseen voi luoda käyttäjän, jonka käyttäjänimi ja salasana tallentuvat tietokantaan, samalla syntyy istunto
- Admin -käyttäjä voi lisätä sovellukseen uuden kasvin
- Jokaiselle kasville on oma sivunsa, josta näkee kasvin tietoja
- Sovelluksessa pystyy kirjautuneena lähettämään palautetta.
- Kasveja voi hakea tietokannasta eri suodattimilla kuten hinta tai kategoria
- Admin voi antaa toiselle käyttäjälle admin -oikeudet, poistaa admin -oikeudet tai poistaa käyttäjän
- Admin -käyttäjä voi poistaa palautteita


Sovelluksen käynnistäminen:

- Kloonaa reposition koneellesi. Tämän jälkene luo samaan kansioon .env -niminen tiedosto.

    .env tiedoston sisällöksi tulee:

  - DATABASE_URL=<tietokannan-paikallinen-osoite>

  - SECRET_KEY=<salainen-avain>
    - Salaisen avaimen voi luoda python3 avulla:
 ```     
       $ python3
        >>>import secrets
        >>>secrets.token_hex(16)
```

- Asenna virtuaaliympäristö ja sovelluksen riippuvuudetkomennoilla:
  - $ python3 -m venv venv
  - $ source venv/bin/activate
  - $ pip install -r ./requirements.txt
- Yhdistä Postgresql ja schema.sql komennolla:
  -  $ psql < schema.sql
- Lopuksi käynnistä sovellus ajamalla kansiossa:
  - $ flask run

Admin oikeuksien testaaminen:
  - luo itsellesi admin salasana python3 avulla ajamalla komennot:
 ``` 
   $ python3
   >>> from werkzeug.security import generate_password_hash
   >>> generate_password_hash('tähän haluamasi salasana')
 ```
 - kopio salasana ja lisää se tietokantaan:
 ```
   $ psql
   =# INSERT INTO Accounts (username, password, rights) VALUES ('valitsemasi käyttäjänimi', 'kopioimasi salasana', 'admin');
 ```
