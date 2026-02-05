#!/bin/bash
set -e

#go to the current dir
cd "$(dirname "$0")"

#create dirs if not there
mkdir -p data
mkdir -p config

echo docker compose pull
docker compose pull

echo docker compose down --remove-orphans
docker compose down --remove-orphans

echo docker compose up --remove-orphans --force-recreate -d
docker compose up --remove-orphans --force-recreate -d

echo docker image prune -f
docker image prune -f

echo docker compose ps -a
docker compose ps -a
