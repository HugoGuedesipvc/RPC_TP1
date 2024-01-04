FROM python:3.12.1-alpine

WORKDIR /app

RUN apk add bash

RUN apk add postgresql-dev gcc python3-dev musl-dev

# install nodemon
RUN apk add --update nodejs npm
RUN npm update npm -g
RUN npm install nodemon -g

RUN apk add g++

# upgrade pip
RUN python -m pip install --upgrade pip
RUN pip install lxml
RUN pip install psycopg2-binary
RUN pip install requests

# dependencies from requirements.txt
COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /data

CMD (sed -i 's/\r$//' ./run.sh) && (chmod +x ./run.sh) && (./run.sh)

ENTRYPOINT python -u main.py