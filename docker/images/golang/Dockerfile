FROM golang:1.21.5-alpine3.19

WORKDIR /usr/src/app


#RUN go get -u github.com/lib/pq
#COPY go.mod ./
#RUN go mod download
# Instalar bash e nodemon
RUN apk add --update bash nodejs npm
RUN npm update npm -g
RUN npm install nodemon -g


ENTRYPOINT (sed -i 's/\r$//' ./run.sh) ; (chmod +x ./run.sh) ; ./run.sh
#ENTRYPOINT ["tail", "-f", "/dev/null"]