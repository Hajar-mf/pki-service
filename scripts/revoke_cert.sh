#!/bin/bash

USER=$1
CERT="users/$USER/$USER.crt"

if [ ! -f "$CERT" ]; then
  echo "Certificat introuvable"
  exit 1
fi

# Révocation
openssl ca -config ca/root/openssl.cnf -revoke "$CERT"

# Génération CRL (OBLIGATOIRE)
openssl ca -config ca/root/openssl.cnf -gencrl -out ca/root/crl/crl.pem

echo "Certificat révoqué + CRL mise à jour"

