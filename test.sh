#!/bin/sh

set -e

# Run all tests in the library.

nosetests3 -v liberty/*
