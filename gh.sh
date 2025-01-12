#!/bin/bash

python3 test/test_suite.py > /dev/null
exit_code=$?
echo "RETURN: $exit_code"


