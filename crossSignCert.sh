#!/bin/bash
 
if [ $# -ne 2 ]; then
  echo 1>&2 "Usage: $0 <domain_to_trust> <path_to_cert_to_cross_sign>"
  echo 1>&2 "Ex: $0 example.org certificate.pem"
  exit 1
fi
 
set -x
 
DOMAIN=$1
CERT_TO_CROSS_SIGN=$2
CROSS_SIGNED_CERT=cross-signed-$(basename ${CERT_TO_CROSS_SIGN})
 
CA_KEY=cross-sign-ca.pem.key
CA_CERT=cross-sign-ca.pem.cer
CERTS_DIR=cross-signed-certs
 
mkdir -p ${CERTS_DIR}
 
OPENSSL_CONFIG="nameConstraints=critical,permitted;DNS:.${DOMAIN},permitted;DNS:${DOMAIN}"
# Re-sign CERT with your own trusted CA and add nameConstraints to only allow certain domains
openssl x509 \
  -in ${CERT_TO_CROSS_SIGN} \
  -CA ${CA_CERT} \
  -CAkey ${CA_KEY} \
  -set_serial 47 \
  -sha256 \
  -extfile <(echo "${OPENSSL_CONFIG}") \
  -out ${CERTS_DIR}/${CROSS_SIGNED_CERT}
