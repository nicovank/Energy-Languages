FROM --platform=linux/amd64 ubuntu:latest

VOLUME [ "/root/data" ]

# General.
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata
RUN apt install -y git cmake ninja-build sudo curl wget pkg-config gnupg

COPY docker/keys /root/Energy-Languages/docker/keys
RUN gpg --import /root/Energy-Languages/docker/keys/*

# C++.
ARG CLANG_VERSION=17
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
ARG RUST_VERSION=1.71.1
RUN wget --no-verbose https://static.rust-lang.org/dist/rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz
RUN wget --no-verbose https://static.rust-lang.org/dist/rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz.asc
RUN gpg --verify rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz.asc rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz
RUN tar -xzf rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz
RUN ./rust-${RUST_VERSION}-x86_64-unknown-linux-gnu/install.sh
RUN rm rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz rust-${RUST_VERSION}-x86_64-unknown-linux-gnu.tar.gz.asc

# Java.
ARG JAVA_VERSION=21+35
ARG JAVA_CHECKSUM=82f64c53acaa045370d6762ebd7441b74e6fda14b464d54d1ff8ca941ec069e6
RUN apt install -y libfastutil-java
RUN wget --no-verbose https://github.com/adoptium/temurin21-binaries/releases/download/jdk-${JAVA_VERSION}/OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz
RUN echo "${JAVA_CHECKSUM} OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz" | sha256sum --check
RUN tar -C /usr/local --strip-components=1 -xzf OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz
RUN rm OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz

# Go.
# https://go.dev/dl/
ARG GO_VERSION=1.21.0
ARG GO_CHECKSUM=d0398903a16ba2232b389fb31032ddf57cac34efda306a0eebac34f0965a0742
RUN wget --no-verbose https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
RUN echo "${GO_CHECKSUM} go${GO_VERSION}.linux-amd64.tar.gz" | sha256sum --check
RUN tar -C /usr/local --strip-components=1 -xzf go${GO_VERSION}.linux-amd64.tar.gz
RUN rm go${GO_VERSION}.linux-amd64.tar.gz

# C#.
# https://dotnet.microsoft.com/en-us/download/dotnet
ARG DOTNET_VERSION=7.0.400
ARG DOTNET_URL=https://download.visualstudio.microsoft.com/download/pr/dbfe6cc7-dd82-4cec-b267-31ed988b1652/c60ab4793c3714be878abcb9aa834b63/dotnet-sdk-${DOTNET_VERSION}-linux-x64.tar.gz
ARG DOTNET_CHECKSUM=4cfeedb8e99ffd423da7a99159ee3f31535fd142711941b8206542acb6be26638fbd9a184a5d904084ffdbd8362c83b6b2acf9d193b2cd38bf7f061443439e3c
RUN wget --no-verbose ${DOTNET_URL}
RUN echo "${DOTNET_CHECKSUM} dotnet-sdk-${DOTNET_VERSION}-linux-x64.tar.gz" | sha512sum --check
RUN tar -C /usr/local/bin -xzf dotnet-sdk-${DOTNET_VERSION}-linux-x64.tar.gz
RUN rm dotnet-sdk-${DOTNET_VERSION}-linux-x64.tar.gz

# Node.js.
# https://nodejs.org/en/download
ARG NODE_VERSION=18.17.1
ARG NODE_CHECKSUM=07e76408ddb0300a6f46fcc9abc61f841acde49b45020ec4e86bb9b25df4dced
RUN wget --no-verbose https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz
RUN echo "${NODE_CHECKSUM} node-v${NODE_VERSION}-linux-x64.tar.xz" | sha256sum --check
RUN tar -C /usr/local --strip-components=1 -xJf node-v${NODE_VERSION}-linux-x64.tar.xz
RUN rm node-v${NODE_VERSION}-linux-x64.tar.xz

# TypeScript.
# https://www.npmjs.com/package/typescript
ARG TYPESCRIPT_VERSION=5.1.6
RUN npm install -g typescript@${TYPESCRIPT_VERSION}

# PHP.
# https://www.php.net/downloads.php
ARG PHP_VERSION=8.2.9
ARG PHP_CHECKSUM=5fac52041335cacfb5845aeff2303f92403925338a0285f2e160feebcb840f04
# https://github.com/php/php-src#building-php-source-code
RUN apt install -y pkg-config build-essential autoconf bison re2c libxml2-dev libsqlite3-dev
RUN wget --no-verbose https://www.php.net/distributions/php-${PHP_VERSION}.tar.gz
RUN echo "${PHP_CHECKSUM} php-${PHP_VERSION}.tar.gz" | sha256sum --check
RUN tar -xzf php-${PHP_VERSION}.tar.gz
RUN cd php-${PHP_VERSION} && ./configure --enable-pcntl --enable-shmop --enable-sysvmsg --with-gmp && make -j && make install
RUN rm -rf php-${PHP_VERSION}.tar.gz php-${PHP_VERSION}

# Python.
ARG PYTHON_VERSION=3.11.4
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
ARG PYPY_VERSION=7.3.12
ARG PYPY_PYTHON_VERSION=3.10
ARG PYPY_CHECKSUM=6c577993160b6f5ee8cab73cd1a807affcefafe2f7441c87bd926c10505e8731
RUN wget --no-verbose https://downloads.python.org/pypy/pypy${PYPY_PYTHON_VERSION}-v${PYPY_VERSION}-linux64.tar.bz2
RUN echo "${PYPY_CHECKSUM} pypy${PYPY_PYTHON_VERSION}-v${PYPY_VERSION}-linux64.tar.bz2" | sha256sum --check
RUN tar -C /usr/local -xjf pypy${PYPY_PYTHON_VERSION}-v${PYPY_VERSION}-linux64.tar.bz2
RUN ln -s /usr/local/pypy${PYPY_PYTHON_VERSION}-v${PYPY_VERSION}-linux64/bin/pypy3 /usr/local/bin/pypy3
RUN rm pypy${PYPY_PYTHON_VERSION}-v${PYPY_VERSION}-linux64.tar.bz2

# Lua.
ARG LUA_VERSION=5.4.6
ARG LUA_CHECKSUM=7d5ea1b9cb6aa0b59ca3dde1c6adcb57ef83a1ba8e5432c0ecd06bf439b3ad88
RUN wget --no-verbose https://www.lua.org/ftp/lua-${LUA_VERSION}.tar.gz
RUN echo "${LUA_CHECKSUM} lua-${LUA_VERSION}.tar.gz" | sha256sum --check
RUN tar -xzf lua-${LUA_VERSION}.tar.gz
RUN cd lua-${LUA_VERSION} && make -j && make install
RUN rm lua-${LUA_VERSION}.tar.gz

# LuaJIT.
ARG LUAJIT_COMMIT=93e87998b24021b94de8d1c8db244444c46fb6e9
RUN git clone https://luajit.org/git/luajit.git
RUN cd luajit && git checkout ${LUAJIT_COMMIT} && make -j && make install
RUN rm -rf luajit

# Ruby.
# Most Ruby benchmarks rely on an older Ruby version.
# We fix it to 2.7.8, the latest version where the required API is deprecated but exists.
# Steps here are taken from rbenv.
RUN wget --no-verbose https://www.openssl.org/source/old/1.1.1/openssl-1.1.1w.tar.gz
RUN echo "76fbf3ca4370e12894a408ef75718f32cdab9671 openssl-1.1.1w.tar.gz" | sha1sum --check
RUN tar -xzf openssl-1.1.1w.tar.gz
RUN cd openssl-1.1.1w && ./config "--prefix=/ruby-openssl" "--openssldir=/ruby-openssl/ssl" zlib-dynamic no-ssl3 shared && make -j && make install_sw install_ssldirs
RUN rm -rf openssl-1.1.1w.tar.gz openssl-1.1.1w
RUN wget --no-verbose https://cache.ruby-lang.org/pub/ruby/2.7/ruby-2.7.8.tar.gz
RUN echo "c2dab63cbc8f2a05526108ad419efa63a67ed4074dbbcf9fc2b1ca664cb45ba0 ruby-2.7.8.tar.gz" | sha256sum --check
RUN tar -xzf ruby-2.7.8.tar.gz
RUN cd ruby-2.7.8 && ./configure "--with-openssl-dir=/ruby-openssl" --enable-shared --with-ext=openssl,psych,+ && make -j && make install
RUN rm -rf ruby-2.7.8.tar.gz ruby-2.7.8

# JRuby.
# On the other hand, the API seems perfectly fine on the latest JRuby version.
ARG JRUBY_VERSION=9.4.8.0
ARG JRUBY_CHECKSUM=347b6692bd9c91c480a45af25ce88d77be8b6e4ac4a77bc94870f2c5b54bc929
RUN wget --no-verbose https://repo1.maven.org/maven2/org/jruby/jruby-dist/${JRUBY_VERSION}/jruby-dist-${JRUBY_VERSION}-bin.tar.gz
RUN echo "${JRUBY_CHECKSUM} jruby-dist-${JRUBY_VERSION}-bin.tar.gz" | sha256sum --check
RUN tar -C /usr/local --strip-components=1 -xzf jruby-dist-${JRUBY_VERSION}-bin.tar.gz
RUN rm -rf jruby-dist-${JRUBY_VERSION}-bin.tar.gz

WORKDIR /root/Energy-Languages
COPY fasta-5000000.txt fasta-5000000.txt
COPY fasta-25000000.txt fasta-25000000.txt
COPY fasta-800000000.txt fasta-800000000.txt
COPY benchmarks benchmarks
COPY experiments experiments
COPY scripts scripts
ENTRYPOINT [ "python3", "-m", "scripts.measure", "-o", "/root/data" ]
