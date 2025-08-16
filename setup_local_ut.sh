#!/bin/bash +ex
REBUILD=${1:-ok}
if [ "$REBUILD" == "ok" ]; then
        docker container rm server-ut
        docker image rm server
	DOCKER_BUILDKIT=1 docker compose build
fi;
docker compose up -d --remove-orphans
echo "To run server"
echo fastapi run main.py --port 8000
echo alembic revision --autogenerate -m "init"
echo alembic upgrade head
docker exec -it server-ut /bin/bash