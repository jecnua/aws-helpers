#!/usr/bin/env bash

# Don't use argv
# Use https://docs.python.org/2/library/argparse.html
no_argv_test=$(grep -l --include=\*.py -R 'argv' . | wc -l)
if [[ $no_argv_test -gt 0 ]]
then
  grep -l -R 'argv' .
  # echo "ERROR"
  exit 1
fi
