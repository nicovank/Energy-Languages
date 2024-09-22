FROM ubuntu:latest

VOLUME [ "/root/data" ]

# General.
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata
RUN apt install -y git cmake ninja-build sudo curl wget pkg-config gnupg

COPY docker /root/Energy-Languages/docker
RUN gpg --import /root/Energy-Languages/docker/keys/*

# C++.
ARG CLANG_VERSION=19
RUN apt install -y lsb-release wget software-properties-common gnupg
RUN curl -sSf https://apt.llvm.org/llvm.sh | bash -s -- ${CLANG_VERSION} all
ENV CC=clang-${CLANG_VERSION}
ENV CXX=clang++-${CLANG_VERSION}
RUN ln -s /usr/bin/llvm-ar-${CLANG_VERSION} /usr/bin/llvm-ar
RUN ln -s /usr/bin/llvm-profdata-${CLANG_VERSION} /usr/bin/llvm-profdata

# C/C++ libraries.
RUN apt install -y libapr1-dev libgmp-dev libpcre3-dev libboost-regex-dev

# Rust.
# https://forge.rust-lang.org/infra/other-installation-methods.html#standalone-installers
ARG RUST_VERSION=1.81.0
RUN wget --no-verbose https://static.rust-lang.org/dist/rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz
RUN wget --no-verbose https://static.rust-lang.org/dist/rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz.asc
RUN gpg --verify rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz.asc rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz
RUN tar -xzf rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz
RUN ./rust-${RUST_VERSION}-x86_64-unknown-linux-gnu/install.sh
RUN rm rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz.asc

# Java.
ARG JAVA_VERSION=21.0.4+7
ARG JAVA_CHECKSUM=51fb4d03a4429c39d397d3a03a779077159317616550e4e71624c9843083e7b9
RUN apt install -y libfastutil-java
RUN wget --no-verbose https://github.com/adoptium/temurin21-binaries/releases/download/jdk-${JAVA_VERSION}/OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz
RUN echo "${JAVA_CHECKSUM} OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz" | sha256sum --check
RUN tar -C /usr/local --strip-components=1 -xzf OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz
RUN rm OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz

# Go.
# https://go.dev/dl/
ARG GO_VERSION=1.23.1
ARG GO_CHECKSUM=49bbb517cfa9eee677e1e7897f7cf9cfdbcf49e05f61984a2789136de359f9bd
RUN wget --no-verbose https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
RUN echo "${GO_CHECKSUM} go${GO_VERSION}.linux-amd64.tar.gz" | sha256sum --check
RUN tar -C /usr/local --strip-components=1 -xzf go${GO_VERSION}.linux-amd64.tar.gz
RUN rm go${GO_VERSION}.linux-amd64.tar.gz

# C#.
# https://dotnet.microsoft.com/en-us/download/dotnet
ARG DOTNET_VERSION=8.0.401 # 8.0.8.
ARG DOTNET_URL=https://download.visualstudio.microsoft.com/download/pr/db901b0a-3144-4d07-b8ab-6e7a43e7a791/4d9d1b39b879ad969c6c0ceb6d052381/dotnet-sdk-8.0.401-linux-x64.tar.gz
ARG DOTNET_CHECKSUM=4d2180e82c963318863476cf61c035bd3d82165e7b70751ba231225b5575df24d30c0789d5748c3a379e1e6896b57e59286218cacd440ffb0075c9355094fd8c
RUN wget --no-verbose ${DOTNET_URL}
RUN echo "${DOTNET_CHECKSUM} dotnet-sdk-${DOTNET_VERSION}-linux-x64.tar.gz" | sha512sum --check
RUN tar -C /usr/local/bin -xzf dotnet-sdk-${DOTNET_VERSION}-linux-x64.tar.gz
RUN rm dotnet-sdk-${DOTNET_VERSION}-linux-x64.tar.gz

# Node.js.
# https://nodejs.org/en/download
ARG NODE_VERSION=20.17.0
ARG NODE_CHECKSUM=a24db3dcd151a52e75965dba04cf1b3cd579ff30d6e0af9da1aede4d0f17486b
RUN wget --no-verbose https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz
RUN echo "${NODE_CHECKSUM} node-v${NODE_VERSION}-linux-x64.tar.xz" | sha256sum --check
RUN tar -C /usr/local --strip-components=1 -xJf node-v${NODE_VERSION}-linux-x64.tar.xz
RUN rm node-v${NODE_VERSION}-linux-x64.tar.xz

# TypeScript.
# https://www.npmjs.com/package/typescript
ARG TYPESCRIPT_VERSION=5.6.2
RUN npm install -g typescript@${TYPESCRIPT_VERSION}

# PHP.
# https://www.php.net/downloads.php
ARG PHP_VERSION=8.3.11
ARG PHP_CHECKSUM=b93a69af83a1302543789408194bd1ae9829e116e784d578778200f20f1b72d4
# https://github.com/php/php-src#building-php-source-code
RUN apt install -y pkg-config build-essential autoconf bison re2c libxml2-dev libsqlite3-dev
RUN wget --no-verbose https://www.php.net/distributions/php-${PHP_VERSION}.tar.gz
RUN echo "${PHP_CHECKSUM} php-${PHP_VERSION}.tar.gz" | sha256sum --check
RUN tar -xzf php-${PHP_VERSION}.tar.gz
RUN cd php-${PHP_VERSION} && ./configure --enable-pcntl --enable-shmop --enable-sysvmsg --with-gmp && make -j && make install
RUN rm -rf php-${PHP_VERSION}.tar.gz php-${PHP_VERSION}

# Python.
ARG PYTHON_VERSION=3.12.6
# https://devguide.python.org/getting-started/setup-building/index.html#build-dependencies
RUN apt install -y build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev
RUN wget --no-verbose https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz
RUN wget --no-verbose https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz.asc
RUN gpg --verify Python-${PYTHON_VERSION}.tar.xz.asc Python-${PYTHON_VERSION}.tar.xz
RUN tar -xJf Python-${PYTHON_VERSION}.tar.xz
RUN cd Python-${PYTHON_VERSION} && ./configure --enable-optimizations --with-lto && make -j && make install
RUN rm -rf Python-${PYTHON_VERSION}.tar.xz Python-${PYTHON_VERSION}.tar.xz.asc Python-${PYTHON_VERSION}

# Python dependencies.
RUN python3 -m pip install --upgrade pip
COPY benchmarks/Python/requirements.txt /root/Energy-Languages/
RUN python3 -m pip install -r /root/Energy-Languages/requirements.txt
COPY scripts/requirements.txt /root/Energy-Languages/
RUN python3 -m pip install -r /root/Energy-Languages/requirements.txt

# PyPy.
ARG PYPY_VERSION=7.3.17
ARG PYPY_PYTHON_VERSION=3.10
ARG PYPY_CHECKSUM=fdcdb9b24f1a7726003586503fdeb264fd68fc37fbfcea022dcfe825a7fee18b
RUN wget --no-verbose https://downloads.python.org/pypy/pypy${PYPY_PYTHON_VERSION}-v${PYPY_VERSION}-linux64.tar.bz2
RUN echo "${PYPY_CHECKSUM} pypy${PYPY_PYTHON_VERSION}-v${PYPY_VERSION}-linux64.tar.bz2" | sha256sum --check
RUN tar -C /usr/local -xjf pypy${PYPY_PYTHON_VERSION}-v${PYPY_VERSION}-linux64.tar.bz2
RUN ln -s /usr/local/pypy${PYPY_PYTHON_VERSION}-v${PYPY_VERSION}-linux64/bin/pypy3 /usr/local/bin/pypy3
RUN rm pypy${PYPY_PYTHON_VERSION}-v${PYPY_VERSION}-linux64.tar.bz2

# Lua.
ARG LUA_VERSION=5.4.7
ARG LUA_CHECKSUM=9fbf5e28ef86c69858f6d3d34eccc32e911c1a28b4120ff3e84aaa70cfbf1e30
RUN wget --no-verbose https://www.lua.org/ftp/lua-${LUA_VERSION}.tar.gz
RUN echo "${LUA_CHECKSUM} lua-${LUA_VERSION}.tar.gz" | sha256sum --check
RUN tar -xzf lua-${LUA_VERSION}.tar.gz
RUN cd lua-${LUA_VERSION} && make -j && make install
RUN rm lua-${LUA_VERSION}.tar.gz

# LuaJIT.
ARG LUAJIT_COMMIT=87ae18af97fd4de790bb6c476b212e047689cc93
RUN git clone https://luajit.org/git/luajit.git
RUN cd luajit && git checkout ${LUAJIT_COMMIT} && make -j && make install
RUN rm -rf luajit

WORKDIR /root/Energy-Languages
COPY fasta-5000000.txt fasta-5000000.txt
COPY fasta-25000000.txt fasta-25000000.txt
COPY fasta-800000000.txt fasta-800000000.txt
COPY benchmarks benchmarks
COPY experiments experiments
COPY scripts scripts
ENTRYPOINT [ "python3", "-m", "scripts.measure", "-o", "/root/data" ]
