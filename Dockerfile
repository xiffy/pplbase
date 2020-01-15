FROM python:3.7

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY *.py /app/
COPY static/* /app/static/
COPY templates/* /app/templates/

#RUN git clone git@github.com:xiffy/pplbase.git

CMD ls -latr
