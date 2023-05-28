#!/usr/bin/env bash
#

#!/usr/bin/env bash
#

set -euo pipefail
set -x

usage() {
  echo 'setup_netdata.sh <SOME-UUID>'
}

# Parse CLI arguments
room_id="${1:-not_provided}"
if [[ "${room_id}" = "not_provided" ]]; then
  usage
  exit 1
fi

# download script
wget -O /tmp/netdata-kickstart.sh https://my-netdata.io/kickstart.sh

# exceute script
sh \
  /tmp/netdata-kickstart.sh \
  --non-interactive \
  --reinstall \
  --no-updates \
  --disable-telemetry \
  --stable-channel \
  --claim-token SUxUQRVWYO1gLGAOp341aTkq5J3J4gMSNSpluAGn4bJMID_32Sv4j71xUCftvcNBb4C1tmli4ZeT485UZbwEi-xPqIIpVi8Q01zil9gIK3D04gwMEcOzD-oWgYrZhY4Lp062u4A \
  --claim-rooms "${room_id}" \
  --claim-url https://app.netdata.cloud

# cleanup
rm -rf /tmp/netdata-kickstart.sh
