FROM python:3.7

EXPOSE 5000

WORKDIR /app

COPY pplbase/requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY pplbase/*.py /app/
COPY pplbase/static /app/static/
COPY pplbase/templates /app/templates/

CMD ["flask", "run", "--host=0.0.0.0"]
