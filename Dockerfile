FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# ENV APP_MODULE src.__main__:app

EXPOSE 8000

COPY ./requirements.txt /app/requirements.txt

RUN python3 -m pip install -U pip --no-input --no-cache-dir && \
    python3 -m pip install -U setuptools --no-input --no-cache-dir && \
    python3 -m pip install -r requirements.txt --no-input --no-cache-dir

COPY ./src /app/src
COPY ./temp /app/temp