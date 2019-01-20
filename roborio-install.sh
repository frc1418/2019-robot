#!/usr/bin/env bash

robotpy-installer install-robotpy
robotpy-installer install-opkg $(< roborio-dependencies.txt)
