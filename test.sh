#!/bin/sh

# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: GPL-3.0-or-later

set -e

# Run all tests in the library.

pytest src/liberty/*
