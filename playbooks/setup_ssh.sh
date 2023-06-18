#!/usr/bin/env bash

set -Eeuo pipefail

set -x

token_url='http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fvault.azure.net'
secret_url='https://ppw-dev-kv.vault.azure.net/secrets/ppw-dev-infra-compute-ssh-key?api-version=2016-10-01'

echo "Retrieve access_token"
echo "timeout 5 curl --fail --silent ${token_url} -H Metadata:true | jq -r '.access_token'"
access_token="$(timeout 5 curl --fail --silent "${token_url}" -H Metadata:true | jq -r '.access_token')"
echo "${access_token}"

: "Retrieve SSH private key"
id_rsa=$(timeout 5 curl --fail --silent "${secret_url}" -H "Authorization: Bearer ${access_token}" | jq -r '.value')

: "Store to disk"
mkdir -p ~/.ssh
echo "${id_rsa}" > ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa

cat <<EOF > ~/.ssh/config
Host *

    # Keep alive
    # Send a "keep alive" signal to the server every 120 seconds
    # And send up to 10 such signals
    ServerAliveInterval 120
    ServerAliveCountMax 10

    # Speed up ssh
    # From https://wiki.archlinux.org/index.php/Secure_Shell#Speeding_up_SSH
    ControlMaster auto
    ControlPersist yes
    ControlPath /tmp/ssh-%r@%h:%p

    # bypass IPV6 lookup
    AddressFamily inet

    PreferredAuthentications=publickey
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
EOF
