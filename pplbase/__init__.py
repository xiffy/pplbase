import os
import time
from elasticsearch_dsl import connections, Index

# to connect to anything different from 'localhost' set ELASTIC_HOSTS to a space-separated-list (or single value)
# see Dockerfile and docker-compose.yml for further explanation

hosts = os.environ.get('ELASTIC_HOSTS', 'localhost').split(" ")
connections.create_connection(hosts=hosts)
endtime = time.time() + 30

while time.time() < endtime:
    try:
        Index('softwareprofs').exists()
        break
    except:
        print('.', end='')
        time.sleep(2)

