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

#### Docker
Of je gebruikt docker en docker-compose in de project root staat een Dockerfile en een docker-compose.yml. De dockerfile gebruikt Docker om de flask-python applicatie te kunnen draaien. Voor elasticsearch gebruik ik een default image (zonder te builden)

```
git clone git@github.com:xiffy/pplbase.git 
docker-compose build
docker-compose run
```
c'est tout. Ook nu kan je op http://localhost:5000/ de applicatie draaien.




    
TODO:
 - [ ] Testen schrijven
 - [x] Dockerize elastic
 - [x] Dockerize pplbase
 - [ ] setup.py

