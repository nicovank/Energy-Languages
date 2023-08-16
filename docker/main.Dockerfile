FROM ubuntu:22.04

VOLUME [ "/lib/modules", "/root/data" ]

WORKDIR /root
RUN apt update

# General.
RUN apt install -y git cmake ninja-build build-essential python3 python3-pip sudo curl wget pkg-config
# C/C++ libraries. (GCC 11)
RUN apt install -y libapr1-dev libgmp-dev libpcre3-dev libboost-regex-dev libhts-dev
# Rust. (1.71.1)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN . "$HOME/.cargo/env"
# Java. (OpenJDK 11)
RUN apt install -y openjdk-11-jdk libfastutil-java
# Go. (1.20.7)
RUN wget https://go.dev/dl/go1.20.7.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C /usr/local -xzf go1.20.7.linux-amd64.tar.gz && rm go1.20.7.linux-amd64.tar.gz
ENV PATH=$PATH:/usr/local/go/bin

# Energy-Languages repo
# RUN git clone https://github.com/nicovank/Energy-Languages.git
RUN mkdir /Energy-Languages
WORKDIR /Energy-Languages
COPY . .

# Python scripts dependencies
WORKDIR /Energy-Languages/scripts
RUN pip install -r requirements.txt
# Generate input
WORKDIR /Energy-Languages
RUN bash ./gen-input.sh

ENTRYPOINT [ "./bench.sh" ]