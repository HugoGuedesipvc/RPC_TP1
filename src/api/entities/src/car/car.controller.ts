import { Controller, Get, Post } from '@nestjs/common';
import { Car } from './car.entity';
import { Body,   Logger, Param, RawBodyRequest, Req } from '@nestjs/common';

@Controller('car')
export class CarController {
  private readonly cars: Car[] = []; // Assuming Car[] is your data store

  @Get()
  findAll() {
    return this.cars;
  }

  @Post()
  createCar(@Req() req: RawBodyRequest<Request>) {
    const r = JSON.parse(req.rawBody.toString())
    // Create a new car with statically defined values
    const newCar: Car = {
      id: r['ID'], // Generating a random ID for simplicity
      country: r['Country'],
      personId: r['PersonID'],
      carId: r['CardID'],
      creditCardId: r['CreditCardID'],
      latitude: r['Latitude'],
      longitude: r['Longitude'],
    };

    // Add the new car to the data store
    this.cars.push(newCar);

    return newCar;
  }
}
