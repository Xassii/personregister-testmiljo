# Personregister testmiljö

## Syfte
Inlämmningsuppgift till kursen "Testdata, testmiljöer och GDPR"

Ett python programm för att skapa testdata och spara den i databaser. Fins enhetstest för att säkerställa att funktionalliteten fungerar. Dockerfile och docker-compose för att köra programmet i samma miljö oavsätt vilken dator det körs i.

## Dependencies
Docker\
Python 3.14

## Kör instruktioner
### Bara appen
- CD till filen app.py ligger i
- Start appen med "python app.py"
- Tryck ctrl-c för att avsluta

### Kör enhetstesten
- CD till filen app.py ligger i
- Kör "python -m pytest tests/"

### Med docker
- CD till filen app.py ligger i
- Start docker:
  - Kör "docker compose up -d" om du inte byggt containern ännu
  - Annars kan du köra "docker compose start"
- Avsluta programmet
  - Stoppa containern med "docker compose stop"
  - Stoppa och ta bort containern med "docker compose down"

### Kör enhetstesten i docker
- Se till att containern körs
- CD till filen app.py ligger i
- Kör "docker exec journal-app python -m pytest tests/"

## Arkitektur
### Programmet
Programmet innehåller tre python filer:
- app.py
- better_faker_sve.py
- user_db.py

#### user_db.py
Innehåller en class för att skapa och hantera användar databaser. När ett UserDB object initialiseras kopplar den upp sig till den angivna databasen och ser till att ett table med columnerna id, email och name skapas om det inte finns.

Classen innehåller metoder för att se hur många och vilka användare finns i databasen, söka efter användare, lägga till och ta bort användare sammt att tömma hela databasen.

#### better_faker_sve.py
En class som använder faker för att skapa användare men har metod för att skapa epost som baseras på användarens namn samt att få ett namn och matchande email tillsammans.

#### app.py
Ett programm som skapar en databas med fejk användare och anonymmiserar de användarna. Validerar sen att fejkanvändarna är GDPR säkra med jämmna mellanrum.

### Enhetstester
Det finns två filer för enhetstest:
- test_better_faker_sve.py
- test_user_db.py

De testar funktionaliteten i better_faker_sve.py och user_db.py respektivt.

För att automatiskt testa koden finns:
- build-test.yml

### Docker
För att säkerställa att programmet kan köras oavsätt dator finns:
- Dockerfile
- docker-compose.yml