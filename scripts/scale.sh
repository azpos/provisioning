#!/usr/bin/env bash
#

set -euo pipefail


display_usage () {
    echo 'Scale the VMSS up or down'
    echo 'Usage: ./scale.sh CAPACITY'
}
# Bail out early
if [[ ( $# -gt 1 ) || ( $# -eq 0) ]]; then
    display_usage
    exit 1
fi
# Read CLI arguments using getopt
cli_options=$(getopt -o th --long help -- "$@")
[ $? -eq 0 ] || {
    echo "Incorrect options provided"
    exit 1
}
eval set -- "$cli_options"
# default values
capacity=0
# Parse getopt arguments
while true; do
    case "$1" in
        -h | --help )           display_usage
                                exit 0
                                ;;
        --)                     shift;
                                capacity=$1;
                                break;;
    esac
done

 az vmss scale \
  --resource-group ppw-dev-compute-rg \
  --name ppw-dev-compute-vmss \
  --new-capacity "${capacity}" \
  --output jsonc
