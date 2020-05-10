#!/bin/sh

while true
do
  python3 update_db.py
  #cp users_db ../dbbackend/users_dev
  #exclude travs
  cat users_db |grep -v trav|grep -v Trav|grep -v gay|grep -v Gay > ../dbbackend/users_dev
  curl -X GET 127.0.0.1:8080/update
  sleep 60
done
