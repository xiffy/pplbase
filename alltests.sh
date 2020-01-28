#!/bin/bash
#
# Script om pplbase te testen. Schiet een Elasticsearch-conainer de lucht in op een aparte poort
# Dat levert isolatie van de testomgeving op en de vrijheid om fake data in te schieten.
# Start the container

docker run -p 9204:9200 -p 9304:9300 -de "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.5.1

# zet de omgevingsvariabelen op deze elasticsearch-docker
export ELASTIC_HOSTS=localhost:9204
export PYTHONPATH=$PWD:$PYTHONPATH
# wacht totdat de standalone elasticsearch is wakker (ik gok op 15 seconden op dit moment)
sleep 15
elasticdump --output=http://localhost:9204/softwareprofs --input=./test/data/softwareprofs_data.json --type=data
python3 test/test_pplbase.py



