FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
LABEL maintainer="dev@uptickhq.com"
LABEL description="Stateless OAuth reverse HTTP proxy"
COPY ./app /app
