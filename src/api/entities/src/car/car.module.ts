import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CarController } from './car.controller';
import { CarService } from './car.service';
import { Car } from './car.entity'; // Import the Car entity

@Module({
  imports: [TypeOrmModule.forFeature([Car])], // Import the Car entity into the module
  controllers: [CarController],
  providers: [CarService],
})
export class CarModule {}