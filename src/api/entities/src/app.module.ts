import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { CarModule } from './car/car.module'; // Assuming you have a CarsModule
import { Car } from './car/car.entity'; // Import the Car entity

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'is-db',
      port: 5432,
      password: 'is',
      username: 'is',
      entities: [Car], // Include the Car entity here
      database: 'pgrel',
      synchronize: true,
      logging: true,
      autoLoadEntities: true
    }),
    CarModule
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}