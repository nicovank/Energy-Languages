#! /usr/bin/env bash

set -euxo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: sudo docker-java-n.sh <LANGUAGE> <DATA_OUTPUT_DIR>"
    echo "Example: sudo docker-java-n.sh Java docker-default"
    exit 1
fi

if [ ! -d "experiments/$1-N" ]; then
  echo "experiments/$1-N does exist."
  exit 1
fi

for i in {1..20}
do
    docker run -it --rm --privileged -e NNNNN=$i -v `pwd`/data/`hostname -s`/$2:/root/data energy-languages \
        --benchmark-root experiments \
        --languages $1-N \
        --warmup 1 \
        --iterations 5
    mv "$(pwd)/data/$(hostname -s)/$2/$1-N" "$(pwd)/data/$(hostname -s)/$2/$1-$i"
done
