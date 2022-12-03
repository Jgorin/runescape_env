FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive \
    HOME=/root \
    VIRTUAL_ENV=/opt/rs_env/ \
    PATH="$PATH:VIRTUAL_ENV/bin"

RUN apt-get update; \
    apt install -y git libtbb-dev libeigen3-dev build-essential \
    libatlas-base-dev libtbb2 python3-venv libboost-dev freeglut3-dev

RUN python3.10 -m venv $VIRTUAL_ENV; \
    pip install --no-cache-dir --upgrade pip
    
WORKDIR "${HOME}"

RUN git clone "https://github.com/Jgorin/runescape_env"; \
    cd runescape_env/runescape_parser; \
    pip install -r requirements.txt; \
    pip install -e .

RUN echo 'alias scan="python ${HOME}/runescape_env/runescape_parser/src/runescape_parser/scan.py"' >> ~/.bashrc