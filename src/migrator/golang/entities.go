package main

import (
	"encoding/xml"
)

type Entity struct {
	ID   int    `xml:"id,attr"`
	Name string `xml:"first_name,attr"`
}

type Person struct {
	Entity
	LastName string `xml:"last_name,attr"`
}

func (p Person) ToEntity() Entity {
	return Entity{
		ID:   p.ID,
		Name: p.Name,
	}
}

type Car struct {
	Entity
	Brand              string `xml:"brand,attr"`
	Model              string `xml:"model,attr"`
	Color              string `xml:"color,attr"`
	YearOfManufacture  int    `xml:"year_of_manufacture,attr"`
}

func (c Car) ToEntity() Entity {
	return Entity{
		ID:   c.ID,
		Name: c.Name,
	}
}

type CreditCard struct {
	Entity
	CardType string `xml:"card_type,attr"`
}

func (cc CreditCard) ToEntity() Entity {
	return Entity{
		ID:   cc.ID,
		Name: cc.Name,
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
		Name: s.Name,
	}
}