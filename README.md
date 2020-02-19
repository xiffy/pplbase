## :construction_worker_man: Fortezza pplbase

Eenvoudige tag-machine waar medewerkers hun skills kunnen aanvinken. Op basis hiervan kunnen heel snel mensen worden gevonden die een bepaalde combinaie van skills en kennis hebben.

De applicatie is geschreven in Python met Flask als basis.
De data wordt opgeslagen in een Elastiscearch database waarmee er eenvoudig aggragaties op de diverse categorieen kunnen worden gemaakt.

Op dit moment is de applicatie volledig onbeveiligd.

routes:
```/view/<naam>
/update/<naam>
/delete/<naam> 
/new
/search?q=<query>
/suggest/<inp>
/namefinder/<inp>
```

#### Running naked (very localhost)
```sudo apt-get update
sudo apt-get install elasticsearch

git clone git@github.com:xiffy/pplbase.git 
cd pplbase
pip install -r requirements.txt
export FLASK_APP=app/py
export FLASK_ENV=development
flask run
```

Je hebt nu een elasticsearch instantie op de standaard poort 9200 draaien (bereikbaar vanaf localhost en nergens anders), en een webserver luisterend op poort 5000. http://localhost:5000/ levert een maagdelijke PeopleBase. 

ELASTIC_HOST: used inside helper-scripts and for testing where precise location of the database and port is crucial, defaults to: ```localhost:9204```

ELASTIC_HOSTS: space separated list of possible host where Elasticsearch might answer. Eases the use in mixed networks (bridged, nat, docker) defaults to: ```localhost:9200``` possible other values (from docker-compose.yml where 'elastic' is the name of the container) ```elastic localhost```

#### Docker
Of je gebruikt docker en docker-compose. In de project root staat een _Dockerfile_ en een _docker-compose.yml_. De dockerfile gebruikt Docker om de flask-python applicatie te kunnen bouwen en draaien. Voor elasticsearch gebruik ik een default image (zonder te builden)

```
git clone git@github.com:xiffy/pplbase.git 
mkdir -p ~/dockerdisks/pplbase
export PPLBASE_STORE=~/dockerdisks/pplbase
docker-compose build
docker-compose up
```
c'est tout. Ook nu kan je op http://localhost:5000/ de applicatie draaien (Your Milage May Vary). 
ELASTIC_HOSTS: space separated list of possible elasicsearch hosts, he first to answer will be used the name of the host could be a docker-service-name

PPLBASE_STORE: optional variable pointing to the 'local'-side of the storage definition. if not set the literal /c/dockerdisks will be used as a default


    
TODO:
 - [ ] setup.py

