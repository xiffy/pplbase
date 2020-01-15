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
    
TODO:
 - [ ] Testen schrijven
 - [ ] Dockerize elastic
 - [ ] Dockerize pplbase
 - [ ] setup.py

