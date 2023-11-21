#!/bin/sh

echo "Processing file: " $1

filename=$1
# filename=$(basename -- "$1")
extension="${filename##*.}"
filename="${filename%.*}"

java -jar build/libs/Driver-java/evmdis.jar --cfg 100 $(<$1) | tail -n +5 >$filename-cfg.dot
