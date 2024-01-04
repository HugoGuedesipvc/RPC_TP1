package main

import (
	"database/sql"
	"encoding/xml"
	"fmt"
	"log"
	"strings"
	"sync"
	"time"

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

type Entity struct {
	ID   int    `xml:"id,attr"`
	Name string `xml:"name,attr"`
}

type Person struct {
	Entity
	FirstName string `xml:"first_name,attr"`
	LastName  string `xml:"last_name,attr"`
}

func (p Person) ToEntity() Entity {
	return Entity{
		ID:   p.ID,
		Name: fmt.Sprintf("Person ID: %d, first_name: %s, last_name: %s", p.ID, p.FirstName, p.LastName),
	}
}

type Car struct {
	Entity
	Brand             string `xml:"brand,attr"`
	Model             string `xml:"model,attr"`
	Color             string `xml:"color,attr"`
	YearOfManufacture int    `xml:"year_of_manufacture,attr"`
}

func (c Car) ToEntity() Entity {
	return Entity{
		ID:   c.ID,
		Name: fmt.Sprintf("Car ID: %d, brand: %s, model: %s, color: %s, year_of_manufacture: %d", c.ID, c.Brand, c.Model, c.Color, c.YearOfManufacture),
	}
}

type CreditCard struct {
	Entity
	CardType string `xml:"card_type,attr"`
}

func (cc CreditCard) ToEntity() Entity {
	return Entity{
		ID:   cc.ID,
		Name: fmt.Sprintf("CreditCard ID: %d, card_type: %s", cc.ID, cc.CardType),
	}
}

type Sale struct {
	Entity
	Country      string `xml:"country,attr"`
	PersonID     string `xml:"person_id,attr"`
	CarID        string `xml:"car_id,attr"`
	CreditCardID string `xml:"credit_card_id,attr"`
	Latitude     string `xml:"latitude,attr"`
	Longitude    string `xml:"longitude,attr"`
}

func (s Sale) ToEntity() Entity {
	return Entity{
		ID:   s.ID,
		Name: fmt.Sprintf("Sale ID: %d, Country: %s", s.ID, s.Country),
	}
}

func start() {
	fmt.Println("A Iniciar")
}

func extractEntitiesFromXML(xmlData string) ([]Entity, error) {
	var entities []Entity

	type Data struct {
		Persons     []Person     `xml:"Persons>Person"`
		Cars        []Car        `xml:"Cars>Car"`
		CreditCards []CreditCard `xml:"CreditCards>CreditCard"`
		Sales       []Sale       `xml:"Sales>Sales"`
	}

	var data Data

	decoder := xml.NewDecoder(strings.NewReader(xmlData))
	err := decoder.Decode(&data)
	if err != nil {
		return nil, fmt.Errorf("Erro ao decodificar XML: %v", err)
	}

	for _, person := range data.Persons {
		entities = append(entities, person.ToEntity())
	}

	for _, car := range data.Cars {
		entities = append(entities, car.ToEntity())
	}

	for _, creditCard := range data.CreditCards {
		entities = append(entities, creditCard.ToEntity())
	}

	for _, sale := range data.Sales {
		entities = append(entities, sale.ToEntity())
	}

	return entities, nil
}

func processXMLFiles(xmlList []string, db *sql.DB, ch *amqp.Channel) {
	
	wg.Add(1)
	defer wg.Done() 

	var allEntities []Entity 

	for _, xmlData := range xmlList {
		entities, err := extractEntitiesFromXML(xmlData)
		if err != nil {
			log.Printf("Erro ao extrair entidades do XML: %v\n", err)
			continue
		}

		fmt.Println("Entidades extraídas do XML:")
		allEntities = append(allEntities, entities...) 
	}


	for _, entity := range allEntities {
	
		fmt.Printf("ID: %d, Nome: %s\n", entity.ID, entity.Name)

	}

}

//func sendTaskMessage(ch *amqp.Channel, entity Entity) {
	
	// messageType := "import"
	// if strings.Contains(entity.Name, "geographic data") {
	// 	messageType = "update"
	// }

	// messageBody := fmt.Sprintf(`{"type": "%s", "id": %d}`, messageType, entity.ID)

	// err := ch.Publish(
	// 	"exchange_name", 
	// 	"routing_key",   
	// 	false,
	// 	false,
	// 	amqp.Publishing{
	// 		ContentType: "application/json",
	// 		Body:        []byte(messageBody),
	// 	},
	// )
	// if err != nil {
	// 	log.Printf("Erro ao enviar mensagem para o RabbitMQ: %v\n", err)
	// }
//}

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

var rabbitMQChannel *amqp.Channel
var wg sync.WaitGroup

func main() {
	log.Println("Aguardando RabbitMQ...")
	time.Sleep(10 * time.Second)

	conn, err := amqp.Dial("amqp://guest:guest@rabbitmq/")
	if err != nil {
		fmt.Println("Failed Initializing Broker Connection")
		panic(err)
	}
	ch, err := conn.Channel()
	if err != nil {
		fmt.Println(err)
	}
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"TestQueue",
		false,
		false,
		false,
		false,
		nil,
	)

	fmt.Println(q)
	if err != nil {
		fmt.Println(err)
	}

	err = ch.Publish(
		"",
		"TestQueue",
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte("Hello World"),
		},
	)

	if err != nil {
		fmt.Println(err)
	}
    fmt.Println("Successfully Published Message to Queue")

	start()
	fmt.Println("Verificando novos arquivos...")
	db, err := connectDB()
	if err != nil {
		log.Fatal("Erro na conexão com o banco de dados:", err)
	}
	defer db.Close()

	//go func() {
	//	wg.Wait()
	//	rabbitMQChannel.Close()
	//}()

	//checkForNewFiles(db, rabbitMQChannel)


	select {}
}