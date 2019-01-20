#!/usr/bin/env bash

robotpy-installer install-robotpy
robotpy-installer install-opkg $(< roborio-opkgs.txt)
robotpy-installer install-pip $(< roborio-requirements.txt)
