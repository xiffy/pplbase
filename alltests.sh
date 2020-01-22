#!/bin/bash
#
# Script om pplbase te testen. Schiet een Elasticsearch-conainer de lucht in op een aparte poort
# Dat levert isolatie van de testomgeving op en de vrijheid om fake data in te schieten.
# Start the container

docker run -p 9204:9200 -p 9304:9300 -de "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.5.2

export ELASTIC_HOSTS=localhost:9204
export PYTHONPATH=$PWD:$PYTHONPATH
echo $PYTHONPATH
python3 test/test_pplbase.py



