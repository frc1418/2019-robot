#!/usr/bin/env bash

robotpy-installer download-robotpy
robotpy-installer download-opkg $(< roborio-opkgs.txt)
robotpy-installer download-pip $(< roborio-requirements.txt)
