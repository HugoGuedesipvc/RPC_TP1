#!/bin/bash

npm install --save @nestjs/typeorm typeorm pg;
npm install;


npx prisma generate;

if [ "$USE_DEV_MODE" = "true" ];
  then npm run start:dev;
  else npm run start;
fi