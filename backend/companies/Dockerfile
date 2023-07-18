FROM python:3.7-buster

# Configuration defaults
ENV FLASK_ROOT "/opt/api"
ENV HTTP_PORT "8000"
ENV FLASK_USER "www-data"
ARG USER_ID="1000"
ENV FLASK_USER_ID "${USER_ID}"
ENV VENV_NAME ".venv-docker"

# Setup system environment variables neded for python to run smoothly
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# Install system requirements
RUN apt-get update && apt-get install -y \
    # mysql requirements
    # Needed for typed-ast dependency
    build-essential \
    # python requirements
    python3-dev python3-pip python3-venv && \
    # cleanup apt caches to keep image small
    rm -rf /var/lib/apt/lists/*

WORKDIR "$FLASK_ROOT"
ADD requirements.txt .

# Setup Python virtualenv separately from code dir
RUN pip install virtualenv && \
    virtualenv "/opt/$VENV_NAME"
ENV PATH="/opt/$VENV_NAME/bin:${PATH}"

# Install the python dependencies
RUN pip install -r requirements.txt && \
    rm requirements.txt

COPY ./ /opt/api

# Create flask user
RUN userdel "$FLASK_USER" && addgroup --system --gid "$FLASK_USER_ID" "$FLASK_USER" && \
    adduser --system --uid "$FLASK_USER_ID" --no-create-home --ingroup "$FLASK_USER" --shell /bin/false "$FLASK_USER"

RUN chown -R "$FLASK_USER_ID":"$FLASK_USER_ID" "/opt/$VENV_NAME/"

USER "$FLASK_USER"
