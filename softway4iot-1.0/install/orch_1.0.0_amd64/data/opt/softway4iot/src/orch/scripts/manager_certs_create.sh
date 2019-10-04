#!/bin/bash

chmod +x ./create-certs.sh

# Create a CA with the password "yourSecretPassword" and "1000000" days until it wil expire.
# The cert files will be in the directory certs
./create-certs.sh -m ca -pw l@b0r@1NF -t certs -e 1000000

# Create server certificate and key with the password of step 1 "yourSecretPassword", with the servername 
# "myserver.example.com" and "1000000" days until it wil expire. 
./create-certs.sh -m server -h myserver.example.com -pw l@b0r@1NF -t certs -e 1000000

# Create client certificate and key with the password of step 1 "yourSecretPassword", with the clientname "testClient" 
# (the name is interesting if you want to use authorization plugins later) and "1000000" days until it wil expire. 
# The cert files will be in the directory certs
./create-certs.sh -m client -h testClient -pw l@b0r@1NF -t certs -e 1000000
