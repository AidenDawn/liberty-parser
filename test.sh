#!/bin/sh

set -e

# Run all tests in the library.

nosetests -v liberty/*
