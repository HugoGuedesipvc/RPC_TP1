package main

import (
	"bytes"
	"fmt"
	"log"
	"net/http"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

func failOnError(err error, msg string) {
	if err != nil {
		log.Panicf("%s: %s", msg, err)
	}
}

func main_amqp(connStr string, apiEntitiesConnStr string) {
	conn, err := amqp.Dial(connStr)
	for {
		if err != nil {
			fmt.Println("Erro ao inicializar a conexão com o RabbitMQ. Esperar 5seg...")
		} else {
			fmt.Println("Conexao sucesso RabbitMQ")
			break
		}
		time.Sleep(5 * time.Second)
		fmt.Println("Tentar inicializar ...")
		conn, err = amqp.Dial(connStr)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q1, err := ch.QueueDeclare(
		"import-entity-queue", // name
		true,                  // durable
		false,                 // delete when unused
		false,                 // exclusive
		false,                 // no-wait
		nil,                   // arguments
	)
	failOnError(err, "Failed to declare a queue")

	msgs, err := ch.Consume(
		q1.Name, // queue
		"",      // consumer
		true,    // auto-ack
		false,   // exclusive
		false,   // no-local
		false,   // no-wait
		nil,     // args
	)
	failOnError(err, "Failed to register a consumer")

	var forever chan struct{}

	go func() {
		for d := range msgs {
			log.Printf("Received a message: %s", d.Body)
			rest_post(apiEntitiesConnStr, string(d.Body[:]))
		}
	}()

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever
}

func rest_post(connUrl string, xmlAtt string) {
	for {
		r, _ := http.NewRequest("POST", connUrl, bytes.NewBuffer([]byte(xmlAtt)))

		r.Header.Add("Content-Type", "text/plain")
		r.Header.Add("Content-Length", "")
		r.Header.Add("Host", "")

		client := &http.Client{}
		_, err := client.Do(r)

		if err == nil {
			log.Printf("Post to api-entitites (%s) success", connUrl)
			break
		} else {
			log.Printf("Post to api-entitites (%s) error: %s", connUrl, err)
			log.Printf("Retry in 5 sec..")
			time.Sleep(5 * time.Second)
		}
	}

}

func main_simulacao(apiEntitiesConnStr string) {

	for {
		rest_post(apiEntitiesConnStr, simularXml)
		log.Printf(" Simulador sleeping 5 sec")
		time.Sleep(5 * time.Second)
	}
}

func main() {
	modo := "real"
	rabbitMqConnStr := "amqp://guest:guest@rabbitmq/"
	apiEntitiesConnStr := "http://api-entities:3000/car"
	if modo == "simulacao" {
		main_simulacao(apiEntitiesConnStr)
	} else {
		main_amqp(rabbitMqConnStr, apiEntitiesConnStr)
	}

}
