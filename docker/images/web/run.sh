#!/bin/bash

npm install;

export NEXT_PUBLIC_API_PROC_URL=$API_PROC_URL
export PORT=$WEB_PORT

if [ $USE_DEV_MODE = "true" ];
  then
    npm run dev;
  else
    npm run build;
    npm run start;
fi