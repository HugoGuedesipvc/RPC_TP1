#!/bin/bash

OUTPUT_BIN="main"
go get -u github.com/lib/pq
go get -u github.com/rabbitmq/amqp091-go

# Check if not in dev mode
if [ "$USE_DEV_MODE" != "true" ]; then
  go build -o $OUTPUT_BIN main.go xmlSimular.go
fi

# Execute the project
if [ "$USE_DEV_MODE" = "true" ]; then
  nodemon --exec go run main.go xmlSimular.go ;
else
  ./$OUTPUT_BIN
fi
