#!/bin/bash
NAME=$1
openssl ca -config ca/root/openssl.cnf -revoke users/$NAME/$NAME.crt

