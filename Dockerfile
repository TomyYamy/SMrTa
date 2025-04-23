FROM python:3.10-slim

WORKDIR /workspace

# apt
RUN apt update && apt-get install -y \
  git \
  build-essential \
  cmake pkg-config \
  libgmp3-dev

# Bitwuzla
RUN git clone https://github.com/bitwuzla/bitwuzla
RUN cd bitwuzla && pip install .

# pip
COPY /requirements.txt ./
RUN pip install -r requirements.txt
