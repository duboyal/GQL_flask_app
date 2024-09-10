#!/bin/sh
# wait-for-selenium.sh

echo "waiting for selenny"
set -e

host="$1"
shift
cmd="$@"

until curl --output /dev/null --head --fail "http://$host"; do
  echo "Trying to connect to Selenium at http://$host..."
  sleep 5
done

echo "Selenium is up - executing command"
exec $cmd
