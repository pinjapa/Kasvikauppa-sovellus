# Kasvikauppa-sovellus
Tsoha projektina on suunnitelmissa tehdä ravintolasovellustyyppinen kasvikauppasovellus. 

Sovelluksen nykeinen tila:
- Sovelluksessa pystyy lähettämään palautetta niin, että se tallentuu tietokantaan.
- Sisäänkirjautuessa syntyy käyttäjälle istunto
- Uloskirjautuessa istunto poistuu
- Ensimmäinen versio kasvikaupan kasvien selailusta ja siihen liittyvästä tietokannasta on olemassa
- On aloitettu tekemään käyttäjien luontia tietokantaan

Tavoitteena on vielä:
- Sovellukseen voi luoda käyttäjän, jonka käyttäjänimi ja salasana tallentuvat tietokantaan
- Tietokantoja on tarkoitus laajentaa niin, että kasveista on enemmän tietoja tietokannoissa
- Sivun vierailija voi kirjautuneena antaa palautetta kasvikaupasta ja kasveista
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
