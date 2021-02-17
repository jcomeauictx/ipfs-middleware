#!/bin/bash
 
set -x
 
TMP_DIR=$(mktemp -d -t cert-XXXXXXXXXX)
CA_KEY=cross-sign-ca.pem.key
CA_CSR=${TMP_DIR}/cross-sign-ca.pem.csr
CA_CERT=cross-sign-ca.pem.cer
 
# Generate CA Private Key
openssl genpkey \
  -algorithm RSA \
  -out ${CA_KEY} \
  -pkeyopt rsa_keygen_bits:4096
 
# Create CA CSR
openssl req \
  -new \
  -key  ${CA_KEY} \
  -days 5480 \
  -extensions v3_ca \
  -batch \
  -out ${CA_CSR} \
  -utf8 \
  -subj '/CN=My Cross Signing CA'
 
 
OPENSSL_ROOT_CONFIG="
basicConstraints=critical,CA:true
keyUsage=keyCertSign,cRLSign
subjectKeyIdentifier=hash
"
# Self sign CA
openssl x509 \
  -req -sha256 \
  -days 3650 \
  -in ${CA_CSR} \
  -signkey ${CA_KEY} \
  -set_serial 1 \
  -extfile <(echo "${OPENSSL_ROOT_CONFIG}") \
  -out ${CA_CERT}
 
rm -r ${TMP_DIR}
