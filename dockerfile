FROM python:3.6

COPY . ./usr/src/app

ENTRYPOINT ["usr/src/app/docker_start.sh"]