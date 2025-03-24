FROM ubuntu:latest

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata
RUN apt install -y python3 unzip wget

# Required (at least) by fop.
RUN apt install -y fontconfig

# Dacapo.
RUN cd root \
    && wget https://download.dacapobench.org/chopin/dacapo-23.11-MR2-chopin.zip \
    && unzip dacapo-23.11-MR2-chopin.zip \
    && rm dacapo-23.11-MR2-chopin.zip

# Java.
ARG JAVA_VERSION=21.0.4+7
ARG JAVA_CHECKSUM=51fb4d03a4429c39d397d3a03a779077159317616550e4e71624c9843083e7b9
RUN wget --no-verbose https://github.com/adoptium/temurin21-binaries/releases/download/jdk-${JAVA_VERSION}/OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz \
    && echo "${JAVA_CHECKSUM} OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz" | sha256sum --check \
    && tar -C /usr/local --strip-components=1 -xzf OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz \
    && rm OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz

# Copy things.
COPY scripts/RAPL/build/rapl /root/rapl
COPY scripts/run_dacapo.py /root/run_dacapo.py

WORKDIR /root
VOLUME [ "/root/data" ]

ENTRYPOINT [ "python3", "/root/run_dacapo.py", "--copies", "21", "--iterations", "1"]
