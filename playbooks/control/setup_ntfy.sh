#!/usr/bin/env bash
#

set -Eeuo pipefail

source utils.sh
source ~/.bashrc

log "START of: PIPX setup"

python3.9 -m pipx install 'git+https://github.com/pmav99/ntfy.git'

mkdir -p ~/.config/ntfy

cat << EOF > ~/.config/ntfy/ntfy.yml
backends:
  - "teams"
teams:
  webhook_url: "https://eceuropaeu.webhook.office.com/webhookb2/c30cb985-f82c-4d12-b57b-63e848c7917c@b24c8b06-522c-46fe-9080-70926f8dddb1/IncomingWebhook/f36b00fe4b374316b9405e25980ae4a4/0eb06807-09cd-4dfc-917b-ccc7ef0fe999"
EOF

ntfy send ""$(date +'%T.%3N')" Finished provisioning of $(hostname --long)"


log "END of: PIPX setup"
