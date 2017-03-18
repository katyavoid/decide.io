#!/bin/bash

# launch the application
uwsgi --ini /app/coin_flip.ini && /usr/sbin/nginx

# ugly hacks to make it work forever
while true ; do
    sleep 600
    date
done
