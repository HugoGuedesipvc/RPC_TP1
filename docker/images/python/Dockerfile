FROM python:3.9.18-alpine

WORKDIR /app

# install nodemon
RUN apk add nodejs npm
RUN npm install -g npm@10.2.1
RUN npm install -g nodemon

# upgrade pip
RUN python -m pip install --upgrade pip
RUN pip install lxml
RUN pip install psycopg2-binary
RUN pip install requests

# dependencies from requirements.txt
COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /data

ENTRYPOINT python -u main.py