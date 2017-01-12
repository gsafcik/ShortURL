FROM frolvlad/alpine-python3
MAINTAINER Geoff Safcik
LABEL version="0.1"

COPY "$PWD" /app
RUN pip3 install -r /app/requirements.txt

ENTRYPOINT ["python3", "/app/main.py"]