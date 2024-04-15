# Kasvikauppa-sovellus
Tsoha projektina on suunnitelmissa tehdä ravintolasovellustyyppinen kasvikauppasovellus. 

Sovelluksen nykeinen tila:

- Sisäänkirjautuessa syntyy käyttäjälle istunto
- Uloskirjautuessa istunto poistuu
- Ensimmäinen versio kasvikaupan kasvien selailusta ja siihen liittyvästä tietokannasta on olemassa
- Sovellukseen voi luoda käyttäjän, jonka käyttäjänimi ja salasana tallentuvat tietokantaan
- Sovelluksessa pystyy kirjautuneena lähettämään palautetta.

Tavoitteena on vielä:
- Tietokantoja on tarkoitus laajentaa niin, että kasveista on enemmän tietoja tietokannoissa
- Kasveja voi hakea eri suodattimilla esim. hinta ja saatavuus
- Kaupan omistajalla on laajat oikeudet muokata kasvien tietoja

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
