#!/bin/bash
ELASTIC_HOST=${ELASTIC_HOST:-localhost:9204}

#elasticdump --output=http://$ELASTIC_HOST/softwareprofs --input=./test/data/softwareprofs_analyzer.json --type=analyzer
#elasticdump --output=http://$ELASTIC_HOST/softwareprofs --input=./test/data/softwareprofs_mapping.json --type=mapping
elasticdump --output=http://$ELASTIC_HOST/softwareprofs --input=./test/data/softwareprofs_data.json --type=data