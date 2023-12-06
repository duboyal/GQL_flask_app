#!/bin/sh
# wait-for-selenium.sh

set -e

host="$1"
shift
cmd="$@"

until curl --output /dev/null --silent --head --fail "http://$host"; do
  printf '.'
  sleep 5
done

exec $cmd
