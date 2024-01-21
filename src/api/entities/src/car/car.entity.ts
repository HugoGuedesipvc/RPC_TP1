import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class Car {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  country: string;

  @Column()
  personId: string;

  @Column()
  carId: string;

  @Column()
  creditCardId: string;

  @Column()
  latitude: string;

  @Column()
  longitude: string;
}