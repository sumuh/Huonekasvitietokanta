### Sovelluksen käyttäminen paikallisesti

1. Asenna tietokoneelle [Python](https://www.python.org/downloads/) (versio 3.x)
2. Lataa zip-pakattu projekti repositorion Clone or download -> Download ZIP -painikkeesta
3. Pura zip-kansio haluamaasi sijaintiin
4. Konsolin avulla luo projektikansion juureen venv-virtuaaliympäristö komennolla ```python3 -m venv venv```
5. Aktivoi virtuaaliympäristö komennolla ```source venv/bin/activate```
6. Lataa projektin tarvitsemat riippuvuudet komennolla ```pip install -r requirements.txt```
7. Käynnistä sovellus projektikansion juuresta komennolla ```python3 run.py```
8. Mene selaimella osoitteeseen http://localhost:5000/. Sovelluksen pitäisi nyt toimia täällä.

### Sovelluksen lataaminen Herokuun

1. Luo Herokuun käyttäjätunnus. Tarvitset käyttöösi myös [Git-versionhallinnan](https://git-scm.com/downloads).
2. Lataa Herokun [komentorivi-työvälineet](https://devcenter.heroku.com/articles/heroku-cli)
3. Luo Herokuun paikka komennolla ```heroku create *sovelluksen nimi*``` (Nimen voi myös jättää tyhjäksi)
4. Lisää Heroku paikalliseen versionhallintaan komennolla ```git remote add heroku https://git.heroku.com/*sovelluksen nimi herokussa*.git```
