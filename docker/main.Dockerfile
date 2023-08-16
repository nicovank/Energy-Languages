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

# Go. On version update, the checksum should also be updated.
# https://go.dev/dl/
ARG GO_VERSION=1.21.0
RUN wget https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
RUN echo "d0398903a16ba2232b389fb31032ddf57cac34efda306a0eebac34f0965a0742 go${GO_VERSION}.linux-amd64.tar.gz" | sha256sum --check --status
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz && rm go${GO_VERSION}.linux-amd64.tar.gz
ENV PATH=$PATH:/usr/local/go/bin
RUN echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile

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
ENTRYPOINT [ "./docker/bench.sh" ]
