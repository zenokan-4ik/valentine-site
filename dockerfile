# syntax=docker/dockerfile:1

FROM python:3.10-slim-bullseye
WORKDIR /python-docker
COPY requirements.txt requirements.txt
COPY static static
COPY templates templates
RUN pip3 install -r requirements.txt
CMD [ "python3", "-m" , "flask", "run.py", "--host=0.0.0.0"]