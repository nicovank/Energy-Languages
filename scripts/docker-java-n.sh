#! /usr/bin/env bash

set -euxo pipefail

if [ ! -d "experiments/$1-N" ]; then
  echo "experiments/$1-N does exist."
  exit 1
fi

for i in {1..20}
do
    docker run -it --rm --privileged -e NNNNN=$i -v `pwd`/data/`hostname -s`/docker-no-turbo:/root/data energy-languages \
        --benchmark-root experiments \
        --languages $1-N \
        --warmup 1 \
        --iterations 7
    mv "$(pwd)/data/$(hostname -s)/docker-no-turbo/$1-N" "$(pwd)/data/$(hostname -s)/docker-no-turbo/$1-$i"
done
