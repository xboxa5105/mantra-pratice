#!/bin/bash +ex
REBUILD=${1:-ok}
if [ "$REBUILD" == "ok" ]; then
        docker container rm server-ut
        docker image rm server
	DOCKER_BUILDKIT=1 docker compose build
fi;
docker compose up -d --remove-orphans
echo "To run all test: (run the following command)"
echo pytest --log-level=INFO -v --sw tests/
echo "Or with coverage example:"
echo "pytest  --log-level=INFO -v --cov-report term:skip-covered --cov=./adapter tests/adapter/"
docker exec -it server-ut /bin/bash