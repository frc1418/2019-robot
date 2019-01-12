#!/usr/bin/env bash
set -e

# E501 line too long
pycodestyle . --ignore=E501

python3 robot/robot.py test
