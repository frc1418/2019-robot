#!/usr/bin/env bash
set -e

verb="$1"
if [[ -z $verb ]]; then
    echo "No verb provided! Valid verbs: download, install" >&2
fi

robotpy-installer $verb-robotpy
robotpy-installer $verb-opkg $(< roborio-opkgs.txt)
robotpy-installer $verb-pip $(< roborio-requirements.txt)
