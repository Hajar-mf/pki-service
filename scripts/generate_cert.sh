#!/bin/bash

NAME=$1

mkdir users/$NAME

openssl genrsa -out users/$NAME/$NAME.key 2048

openssl req -new -key users/$NAME/$NAME.key -out users/$NAME/$NAME.csr

openssl x509 -req \
-in users/$NAME/$NAME.csr \
-CA ca/root/certs/root.crt \
-CAkey ca/root/private/root.key \
-CAcreateserial \
-out users/$NAME/$NAME.crt \
-days 365

