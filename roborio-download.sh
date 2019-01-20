#!/usr/bin/env bash

robotpy-installer download-robotpy
robotpy-installer download-opkg $(< roborio-dependencies.txt)
