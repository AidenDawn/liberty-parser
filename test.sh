#!/bin/sh

set -e

# Run all tests in the library.

# To use another python version: 
#NOSE="python3.9 $(which nosetests3)"
NOSE=nosetests3
$NOSE -v liberty/*
