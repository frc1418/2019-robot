#!/usr/bin/env bash
set -e

# E501 line too long
pycodestyle . --ignore=E501
# Re-add the line below after basic project structure is set up
# python3 robot/robot.py test
