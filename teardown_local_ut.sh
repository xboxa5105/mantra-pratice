#!/bin/bash +ex
docker-compose down --remove-orphans
docker volume prune -f
docker network prune -f