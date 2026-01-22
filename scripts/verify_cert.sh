#!/bin/bash
NAME=$1
openssl verify -CAfile ca/root/certs/root.crt users/$NAME/$NAME.crt

