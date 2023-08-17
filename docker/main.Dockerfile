FROM ubuntu:latest

VOLUME [ "/root/data" ]

RUN mkdir /root/Energy-Languages
COPY . /root/Energy-Languages

# General.
RUN apt update
RUN apt install -y git cmake ninja-build build-essential sudo curl wget pkg-config gpg
RUN gpg --import /root/Energy-Languages/docker/keys/*

# C/C++ libraries.
RUN apt install -y libapr1-dev libgmp-dev libpcre3-dev libboost-regex-dev libhts-dev

# Rust.
# https://forge.rust-lang.org/infra/other-installation-methods.html#standalone-installers
ARG RUST_VERSION=1.71.1
RUN wget https://static.rust-lang.org/dist/rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz
RUN wget https://static.rust-lang.org/dist/rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz.asc
RUN gpg --verify rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz.asc rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz
RUN tar -xzf rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz
RUN ./rust-${RUST_VERSION}-x86_64-unknown-linux-gnu/install.sh
RUN rm -rf rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz.asc

# Java.
RUN apt install -y openjdk-11-jdk libfastutil-java

# Go.
# https://go.dev/dl/
ARG GO_VERSION=1.21.0
ARG GO_CHECKSUM=d0398903a16ba2232b389fb31032ddf57cac34efda306a0eebac34f0965a0742
RUN wget https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
RUN echo "${GO_CHECKSUM} go${GO_VERSION}.linux-amd64.tar.gz" | sha256sum --check --status
RUN tar -C /usr/local --strip-components=1 -xzf go${GO_VERSION}.linux-amd64.tar.gz
RUN rm go${GO_VERSION}.linux-amd64.tar.gz

# C#.

# Node.js.
# https://nodejs.org/en/download
ARG NODE_VERSION=18.17.1
ARG NODE_CHECKSUM=07e76408ddb0300a6f46fcc9abc61f841acde49b45020ec4e86bb9b25df4dced
RUN wget https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz
RUN echo "${NODE_CHECKSUM} node-v${NODE_VERSION}-linux-x64.tar.xz" | sha256sum --check --status
RUN tar -C /usr/local --strip-components=1 -xJf node-v${NODE_VERSION}-linux-x64.tar.xz
RUN rm -rf node-v${NODE_VERSION}-linux-x64.tar.xz

# PHP.

# Python.
ARG PYTHON_VERSION=3.11.4
# https://devguide.python.org/getting-started/setup-building/index.html#build-dependencies
RUN DEBIAN_FRONTEND=noninteractive apt install -y gdb lcov libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz.asc
RUN gpg --verify Python-${PYTHON_VERSION}.tar.xz.asc Python-${PYTHON_VERSION}.tar.xz
RUN tar -xJf Python-${PYTHON_VERSION}.tar.xz
RUN cd Python-${PYTHON_VERSION} && ./configure --enable-optimizations --with-lto && make -j && make install
RUN rm -rf Python-${PYTHON_VERSION}.tar.xz Python-${PYTHON_VERSION}.tar.xz.asc

# Python scripts dependencies.
RUN python3 -m pip install -r /root/Energy-Languages/scripts/requirements.txt

WORKDIR /root/Energy-Languages
RUN ./gen-input.sh
# TODO Restore.
# ENTRYPOINT [ "./docker/bench.sh" ]
ENTRYPOINT [ "bash" ]
