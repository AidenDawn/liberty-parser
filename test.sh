#!/bin/sh

# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: GPL-3.0-or-later

set -e

# Run all tests in the library.

# To use another python version: 
NOSE="python3.9 $(which nosetests3)"
#NOSE=nosetests3
$NOSE -v liberty/*
