FROM --platform=linux/amd64 ubuntu:latest

VOLUME [ "/root/data" ]

# General.
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata
RUN apt install -y git cmake ninja-build sudo curl wget pkg-config gnupg
RUN apt install -y redis # Required by key-value.

COPY docker/keys /root/LangBench/docker/keys
RUN gpg --import /root/LangBench/docker/keys/*

# C++.
ARG CLANG_VERSION=17
RUN apt install -y lsb-release wget software-properties-common gnupg
RUN curl -sSf https://apt.llvm.org/llvm.sh | bash -s -- ${CLANG_VERSION} all
ENV CC=clang-${CLANG_VERSION}
ENV CXX=clang++-${CLANG_VERSION}
RUN ln -s /usr/bin/llvm-ar-${CLANG_VERSION} /usr/bin/llvm-ar
RUN ln -s /usr/bin/llvm-profdata-${CLANG_VERSION} /usr/bin/llvm-profdata

# Java.
ARG JAVA_VERSION=21+35
ARG JAVA_CHECKSUM=82f64c53acaa045370d6762ebd7441b74e6fda14b464d54d1ff8ca941ec069e6
RUN apt install -y libfastutil-java
RUN wget --quiet https://github.com/adoptium/temurin21-binaries/releases/download/jdk-${JAVA_VERSION}/OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz
RUN echo "${JAVA_CHECKSUM} OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz" | sha256sum --check
RUN tar -C /usr/local --strip-components=1 -xzf OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz
RUN rm OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz

# Go.
# https://go.dev/dl/
ARG GO_VERSION=1.21.0
ARG GO_CHECKSUM=d0398903a16ba2232b389fb31032ddf57cac34efda306a0eebac34f0965a0742
RUN wget --quiet https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
RUN echo "${GO_CHECKSUM} go${GO_VERSION}.linux-amd64.tar.gz" | sha256sum --check
RUN tar -C /usr/local --strip-components=1 -xzf go${GO_VERSION}.linux-amd64.tar.gz
RUN rm go${GO_VERSION}.linux-amd64.tar.gz

# Node.js.
# https://nodejs.org/en/download
ARG NODE_VERSION=18.17.1
ARG NODE_CHECKSUM=07e76408ddb0300a6f46fcc9abc61f841acde49b45020ec4e86bb9b25df4dced
RUN wget --quiet https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz
RUN echo "${NODE_CHECKSUM} node-v${NODE_VERSION}-linux-x64.tar.xz" | sha256sum --check
RUN tar -C /usr/local --strip-components=1 -xJf node-v${NODE_VERSION}-linux-x64.tar.xz
RUN rm node-v${NODE_VERSION}-linux-x64.tar.xz

# Python.
ARG PYTHON_VERSION=3.11.4
# https://devguide.python.org/getting-started/setup-building/index.html#build-dependencies
RUN apt install -y build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev
RUN wget --quiet https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz
RUN wget --quiet https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz.asc
RUN gpg --verify Python-${PYTHON_VERSION}.tar.xz.asc Python-${PYTHON_VERSION}.tar.xz
RUN tar -xJf Python-${PYTHON_VERSION}.tar.xz
RUN cd Python-${PYTHON_VERSION} && ./configure --enable-optimizations --with-lto && make -j && make install
RUN rm -rf Python-${PYTHON_VERSION}.tar.xz Python-${PYTHON_VERSION}.tar.xz.asc Python-${PYTHON_VERSION}

# Python dependencies.
RUN python3 -m pip install --upgrade pip
RUN apt install -y libgmp-dev libmpc-dev
COPY Python/requirements.txt /root/LangBench/
RUN python3 -m pip install -r /root/LangBench/requirements.txt
COPY scripts/requirements.txt /root/LangBench/
RUN python3 -m pip install -r /root/LangBench/requirements.txt

WORKDIR /root/LangBench
# TODO: Fix copy below.
COPY . .
RUN python3 ./benchmark-data/file-server/generate.py
RUN make -C ./benchmark-data/file-server/client/
ENTRYPOINT [ "python3", "-m", "scripts.measure", "-o", "/root/data" ]
