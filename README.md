# Kasvikauppa-sovellus
Tsoha projektina on suunnitelmissa tehdä ravintolasovellustyyppinen kasvikauppasovellus. 

Sovelluksen nykeinen tila:

- Sisäänkirjautuessa syntyy käyttäjälle istunto
- Uloskirjautuessa istunto poistuu
- Sovellukseen voi luoda käyttäjän, jonka käyttäjänimi ja salasana tallentuvat tietokantaan
- Admin -käyttäjä voi lisätä sovellukseen uuden kasvin
- Jokaiselle kasville on oma sivunsa, josta näkee kasvin tietoja
- Sovelluksessa pystyy kirjautuneena lähettämään palautetta.

Tavoitteena on vielä:
- Kasveja voi hakea tietokannasta eri suodattimilla kuten hinta tai kategoria
- Admin -käyttäjä voi poistaa palautteita tai kasveja
- Profiili sivun täydentäminen
- tyyli.css tiedoston luonti ja ukoasun parantaminen

Sovelluksen käynnistäminen:
Koneellesi täytyy luoda tiedosto .env samana kansioon kuin kloonattu repositorio

Sinne tarvitsee:

DATABASE_URL=<tietokannan-paikallinen-osoite>

SECRET_KEY=<salainen-avain>

Asenna ja aktivoi virtuaaliympäristö komennoilla
  - $ python3 -m venv venv
  - $ source venv/bin/activate
  - $ pip install -r ./requirements.txt
  - $ flask run
