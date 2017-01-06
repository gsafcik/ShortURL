FROM frolvlad/alpine-python3
MAINTAINER Geoff Safcik
LABEL version="0.1"

COPY "$PWD" /app
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python3", "/app/main.py"]