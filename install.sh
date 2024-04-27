#!/bin/sh
# Simple installer written for Synology NAS

set -eu

# Run as root
if [ "$(id -u)" -ne 0 ]; then
	        printf 'Script should be run with sudo\n' >&2
			        exit 1
fi

# Setup folders
printf 'Copying watcher script to /volume1/emby_media_watcher\n'
mkdir -p /volume1/emby_media_watcher
cp emby_media_watcher.py /volume1/emby_media_watcher/

printf 'Creating emby media watcher systemd service\n'
cp emby_media_watcher.service /etc/systemd/system/

# Write API key to file without echoing in terminal
stty -echo
printf 'Enter emby API key: '
read EMBY_API_KEY
stty echo
printf '\n'
printf EMBY_API_KEY="$EMBY_API_KEY" > /volume1/emby_media_watcher/.env

# Python virtual environment and dependencies
printf 'Creating python virtual environment and installing dependencies\n'
cd /volume1/emby_media_watcher
/bin/python3 -m venv .venv
/volume1/emby_media_watcher/.venv/bin/python -m pip install requests watchdog
# Pinned version
#/volume1/emby_media_watcher/.venv/bin/python -m pip install --force-reinstall requests==2.31.0 watchdog=4.0.0

# Enable/Start systemd service
printf 'Enabling and starting emby media watcher service\n'
systemctl enable emby_media_watcher.service
systemctl start emby_media_watcher.service
