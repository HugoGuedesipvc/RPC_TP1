import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { NestExpressApplication } from '@nestjs/platform-express';
import { Client } from 'pg';

async function createDatabase() {
  const client = new Client({
    host: 'is-db',
    port: 5432,
    user: 'is',
    password: 'is',
    database: 'postgres', // Connect to the default 'postgres' database
  });

  try {
    await client.connect();
    await client.query('CREATE DATABASE pgrel');
    console.log('Database "pgrel" created successfully.');
  } catch (error) {
    console.error('Database "pgrel" already exists. Continuing...');
  } finally {
    await client.end();
  }
}

async function bootstrap() {
  await createDatabase();

  const app = await NestFactory.create<NestExpressApplication>(AppModule, {
    rawBody: true,
  });
  app.useBodyParser('text', { limit: '10mb' });
  // app.useBodyParser('raw');
  await app.listen(3000);
}
bootstrap();
