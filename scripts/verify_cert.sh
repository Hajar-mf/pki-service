#!/bin/bash

USER=$1
CERT="users/$USER/$USER.crt"
CRL="ca/root/crl/crl.pem"
CA_CERT="ca/root/certs/root.crt"

if [ ! -f "$CERT" ]; then
  echo "Certificat introuvable"
  exit 1
fi

if [ ! -f "$CRL" ]; then
  echo "CRL introuvable (aucun certificat révoqué)"
  exit 1
fi

openssl verify -CAfile "$CA_CERT" -crl_check -CRLfile "$CRL" "$CERT"

