#!/usr/bin/env bash

# Don't use argv
# Use https://docs.python.org/2/library/argparse.html
no_argv_test=$(grep -l -R 'argv' . | grep -v 'validate_me.sh' | wc -l)
if [[ $no_argv_test -gt 0 ]]
then
  echo "ERROR"
fi
