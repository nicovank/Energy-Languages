FROM ubuntu:latest AS builder

# General.
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata
RUN apt install -y git wget

# Set encoding to UTF-8.
RUN apt install -y locales
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8

# Ant.
ARG ANT_VERSION=1.10.15
ARG ANT_CHECKSUM=d78427aff207592c024ff1552dc04f7b57065a195c42d398fcffe7a0145e8d00cd46786f5aa52e77ab0fdf81334f065eb8011eecd2b48f7228e97ff4cb20d16c
RUN wget https://dlcdn.apache.org//ant/binaries/apache-ant-1.10.15-bin.tar.gz \
    && echo "${ANT_CHECKSUM} apache-ant-1.10.15-bin.tar.gz" | sha512sum --check \
    && tar -xzf apache-ant-1.10.15-bin.tar.gz \
    && cp -r apache-ant-1.10.15/bin /usr/local \
    && cp -r apache-ant-1.10.15/lib /usr/local \
    && rm -rf apache-ant-1.10.15-bin.tar.gz apache-ant-1.10.15

# Java versions 8 and 11 are required for the build.
RUN wget --no-verbose https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u442-b06/OpenJDK8U-jdk_x64_linux_hotspot_8u442b06.tar.gz \
    && echo "5b0a0145e7790552a9c8767b4680074c4628ec276e5bb278b61d85cf90facafa OpenJDK8U-jdk_x64_linux_hotspot_8u442b06.tar.gz" | sha256sum --check \
    && tar -C /usr/local --strip-components=1 -xzf OpenJDK8U-jdk_x64_linux_hotspot_8u442b06.tar.gz \
    && rm OpenJDK8U-jdk_x64_linux_hotspot_8u442b06.tar.gz
RUN wget --no-verbose https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.26+4/OpenJDK11U-jdk_x64_linux_hotspot_11.0.26_4.tar.gz \
    && echo "7def4c5807b38ef1a7bb30a86572a795ca604127cc8d1f5b370abf23618104e6 OpenJDK11U-jdk_x64_linux_hotspot_11.0.26_4.tar.gz" | sha256sum --check \
    && mkdir /jdk11 \
    && tar -C /jdk11 --strip-components=1 -xzf OpenJDK11U-jdk_x64_linux_hotspot_11.0.26_4.tar.gz \
    && rm OpenJDK11U-jdk_x64_linux_hotspot_11.0.26_4.tar.gz
ENV JAVA_HOME=/usr/local

# Various DaCapo dependencies.
RUN apt install -y cvs nodejs maven npm python-is-python3 python3 python3-pip subversion
RUN pip install --break-system-packages requests

# DaCapo.
ARG DACAPO_HASH=0db32562cf169730c163d88df2eeb28217ca7d03
RUN git clone https://github.com/dacapobench/dacapobench.git /root/dacapobench
RUN cd /root/dacapobench && git checkout ${DACAPO_HASH}
RUN echo 'jdk.11.home=/jdk11' >> /root/dacapobench/benchmarks/local.properties
COPY docker/DaCapo.patch /root/dacapobench
RUN cd /root/dacapobench && git apply DaCapo.patch
RUN rm /root/dacapobench/DaCapo.patch
RUN cd /root/dacapobench/benchmarks && ant dist



FROM ubuntu:latest AS runner

# General.
RUN apt update
RUN apt install -y wget

# Java.
ARG JAVA_VERSION=21.0.4+7
ARG JAVA_CHECKSUM=51fb4d03a4429c39d397d3a03a779077159317616550e4e71624c9843083e7b9
RUN wget --no-verbose https://github.com/adoptium/temurin21-binaries/releases/download/jdk-${JAVA_VERSION}/OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz \
    && echo "${JAVA_CHECKSUM} OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz" | sha256sum --check \
    && tar -C /usr/local --strip-components=1 -xzf OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz \
    && rm OpenJDK21U-jdk_x64_linux_hotspot_$(echo $JAVA_VERSION | sed s/+/_/).tar.gz

# Copy things.
COPY --from=builder /root/dacapobench/benchmarks /root/benchmarks
COPY scripts/RAPL/build/rapl /root/rapl
WORKDIR /root/benchmarks

VOLUME [ "/root/data" ]
ENTRYPOINT [ "/bin/bash" ]
