# Transfer daemon.json to gateway
sudo scp daemon.json $1@$2:$3

# Copying keys from Gateway Manager to Gateway via scp: $1 gatewaName, $2 IPgateway, $3 path to transfer certs
cd certs
sudo scp ca.pem server-cert.pem server-key.pem $1@$2:$3
