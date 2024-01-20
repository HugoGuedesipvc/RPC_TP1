package main

import (
	"database/sql"
	"encoding/xml"
	"encoding/json"
	"fmt"
	"log"
	"time"
	"reflect"

	_ "github.com/lib/pq"
	"github.com/streadway/amqp"
)

var db_params = map[string]string{
	"host":     "is-db",
	"database": "is",
	"user":     "is",
	"password": "is",
	"port":     "5432",
}

type Data struct {
	XMLName     xml.Name      `xml:"Data"`
	Persons     []Person      `xml:"Persons>Person"`
	Cars        []Car         `xml:"Cars>Car"`
	CreditCards []CreditCard  `xml:"CreditCards>CreditCard"`
	Sales       []Sale        `xml:"Sales>Sales"`
}

type Person struct {
	ID        int    `xml:"id,attr"`
	FirstName string `xml:"first_name,attr"`
	LastName  string `xml:"last_name,attr"`
}

type Car struct {
	ID                int    `xml:"id,attr"`
	Brand             string `xml:"brand,attr"`
	Model             string `xml:"model,attr"`
	Color             string `xml:"color,attr"`
	YearOfManufacture int    `xml:"year_of_manufacture,attr"`
}

type CreditCard struct {
	ID       int    `xml:"id,attr"`
	CardType string `xml:"card_type,attr"`
}

type Sale struct {
	ID            int    `xml:"id,attr"`
	Country       string `xml:"country,attr"`
	PersonID      string `xml:"person_id,attr"`
	CarID         string `xml:"car_id,attr"`
	CreditCardID  string `xml:"credit_card_id,attr"`
	Latitude      string `xml:"latitude,attr"`
	Longitude     string `xml:"longitude,attr"`
}

func loadDataFromXML(xmlData string) (Data, error) {
    var data Data
    err := xml.Unmarshal([]byte(xmlData), &data)
    if err != nil {
        return Data{}, err
    }
    return data, nil
}

func publishEntities(ch *amqp.Channel, entityType string, entities []interface{}) {
	for _, entity := range entities {
		err := publishEntity(ch, entityType, entity)
		if err != nil {
			fmt.Printf("Erro ao publicar %s: %v\n", entityType, err)
		}
	}
}

func printQueueInfo(ch *amqp.Channel, queueName string) {
	queueInfo, err := ch.QueueInspect(queueName)
	if err != nil {
		fmt.Printf("Erro ao obter informações sobre a fila %s: %v\n", queueName, err)
	} else {
		fmt.Printf("Informações sobre a fila %s:\n%+v\n", queueName, queueInfo)
	}
}

func publishEntity(ch *amqp.Channel, entityType string, entity interface{}) error {
	messageBody, err := json.Marshal(entity)
	if err != nil {
		return err
	}

	err = ch.Publish(
		"",
		entityType,
		false,
		false,
		amqp.Publishing{
			ContentType: "application/json",
			Body:        messageBody,
		},
	)
	return err
}

func declareQueues(ch *amqp.Channel) {
	queues := []string{
		"import-entity-queue",
		"update-geographic-data-queue",
	}

	for _, queueName := range queues {
		err := declareQueue(ch, queueName)
		if err != nil {
			fmt.Printf("Erro ao declarar a fila %s: %v\n", queueName, err)
		}
	}
}

func declareQueue(ch *amqp.Channel, queueName string) error {
	_, err := ch.QueueDeclare(
		queueName,
		true,
		false,
		false,
		false,
		nil,
	)
	return err
}

func interfaceSlice(slice interface{}) []interface{} {
	s := reflect.ValueOf(slice)
	if s.Kind() != reflect.Slice {
		panic("interfaceSlice() given a non-slice type")
	}

	var result []interface{}
	for i := 0; i < s.Len(); i++ {
		result = append(result, s.Index(i).Interface())
	}

	return result
}

func main() {
	log.Println("Aguardando RabbitMQ...JOMS16")
	time.Sleep(10 * time.Second)

	conn, err := amqp.Dial("amqp://guest:guest@rabbitmq/")
	if err != nil {
		fmt.Println("Erro ao inicializar a conexão com o RabbitMQ")
		panic(err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		fmt.Println("Erro ao criar o canal RabbitMQ")
		panic(err)
	}
	defer ch.Close()

	db, err := connectDB()
	if err != nil {
		log.Fatal("Erro na conexão com o banco de dados:", err)
	}

	fmt.Println("Verificando novos arquivos...")

	declareQueues(ch)

	go checkForNewFiles(db,ch)

	select {}

}

func connectDB() (*sql.DB, error) {
	connStr := fmt.Sprintf("host=%s dbname=%s user=%s password=%s port=%s sslmode=disable",
		db_params["host"], db_params["database"], db_params["user"], db_params["password"], db_params["port"])

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, err
	}

	err = db.Ping()
	if err != nil {
		return nil, err
	}

	fmt.Println("Conectado ao banco de dados")
	return db, nil
}

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func checkForNewFiles(db *sql.DB, ch *amqp.Channel) {
    ticker := time.NewTicker(1 * time.Second)

    var xmlList []string

    for {
        select {
        case <-ticker.C:
            rows, err := db.Query("SELECT xml FROM imported_documents WHERE updated_on > $1", time.Now().Add(-5*time.Second))
            if err != nil {
                log.Printf("Erro ao consultar o banco de dados: %v\n", err)
                continue
            }
            defer rows.Close()

            for rows.Next() {
                var xmlData string

                err := rows.Scan(&xmlData)
                if err != nil {
                    log.Printf("Erro ao escanear linha: %v\n", err)
                    continue
                }

                xmlList = append(xmlList, xmlData)
            }
            err = rows.Err()
            if err != nil {
                log.Printf("Erro ao iterar pelos resultados: %v\n", err)
            }

            if len(xmlList) > 0 {
                processXMLFiles(xmlList, db, ch)
                xmlList = nil
            }
        }
    }
}

func processXMLFiles(xmlList []string, db *sql.DB, ch *amqp.Channel) {
    for _, xmlData := range xmlList {
        data, err := loadDataFromXML(xmlData)
        if err != nil {
            log.Printf("Erro ao carregar dados do XML: %v\n", err)
            continue
        }

        fmt.Println("Entidades publicadas no RabbitMQ")

        publishEntities(ch, "update-geographic-data-queue", interfaceSlice(data.Sales))
        publishEntities(ch, "import-entity-queue", interfaceSlice(data.Persons))
        publishEntities(ch, "import-entity-queue", interfaceSlice(data.Cars))
        publishEntities(ch, "import-entity-queue", interfaceSlice(data.CreditCards))
        publishEntities(ch, "import-entity-queue", interfaceSlice(data.Sales))
    }

    printQueueInfo(ch, "import-entity-queue")
    printQueueInfo(ch, "update-geographic-data-queue")
}
