FROM python:3.9

RUN apt-get update
RUN apt-get install libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev -y

RUN python3 -m venv /tmp/venv && \
    /tmp/venv/bin/pip install -U pip setuptools && \
    /tmp/venv/bin/pip install poetry

WORKDIR /opt/chess4irc
COPY src .

RUN /tmp/venv/bin/poetry install

ENTRYPOINT ["/tmp/venv/bin/poetry", "run", "python", "chess4irc.py"]
