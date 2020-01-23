#!/bin/bash
# NB. Dit scrip vraagt ELASTIC_HOST in enkelvoud op. De flask-applicatie vraagt de meervoudsvorm op
# default localhost:9200, op een docker connecten met een exotische poortnummer zet je
# export ELASTIC_HOST=dockerhostname:9876
# script is afhankelijk van elasticdump: https://www.npmjs.com/package/elasticdump

ELASTIC_HOST=${ELASTIC_HOST:-localhost:9200}
cp ./test/data/softwareprofs_mapping.json ./test/data/old_mapping.json
cp ./test/data/softwareprofs_data.json ./test/data/old_data.json
cp ./test/data/softwareprofs_analyzer.json ./test/data/old_analyzer.json
rm ./test/data/softwareprofs_*.json
elasticdump --input=http://$ELASTIC_HOST/softwareprofs --output=./test/data/softwareprofs_analyzer.json --type=analyzer
elasticdump --input=http://$ELASTIC_HOST/softwareprofs --output=./test/data/softwareprofs_mapping.json --type=mapping
elasticdump --input=http://$ELASTIC_HOST/softwareprofs --output=./test/data/softwareprofs_data.json --type=data