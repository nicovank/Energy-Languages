#! /usr/bin/env bash

set -euxo pipefail

if [ ! -d "experiments/$1-N" ]; then
  echo "experiments/$1-N does exist."
  exit 1
fi

for i in {1..20}
do
    docker run -it --privileged -e NNNNN=$i -v `pwd`/data/`hostname -s`/docker-default:/root/data energy-languages \
        --languages experiments/$1-N \
        --warmup 1 \
        --iterations 7
    mv "$(pwd)/data/$(hostname -s)/docker-default/experiments/$1-N $(pwd)/data/$(hostname -s)/docker-default/experiments/$1-$i"
done
