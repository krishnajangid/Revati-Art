FROM python:3.10-alpine as base
RUN apk update \
    && apk add --no-cache mariadb-dev

FROM base as base_build
RUN apk add --virtual build-deps gcc musl-dev libffi-dev
COPY requirements.txt /tmp/requirements.txt
RUN pip install --target=/dependencies -r /tmp/requirements.txt

FROM base
WORKDIR /src
COPY --from=base_build /dependencies /usr/local/lib/python3.10/site-packages/
COPY ./src/ /src/
COPY ./entrypoint.sh  /user/local/entrypoint.sh

RUN ["chmod", "+x", "/user/local/entrypoint.sh"]
