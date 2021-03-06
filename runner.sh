#!/bin/bash

#file="scores.txt"

#if [ -f "$file" ] ; then
#    rm "$file"
#fi

# tries=10
# sum=0
# for (( counter=$tries; counter>0; counter-- ))
# do
# python3 student.py
# done

rm results.txt
touch results.txt
for i in {0..9};do
  python3 server.py --seed $RANDOM --port $(( $i + 6000 )) &
  python3 viewer.py --port $(( $i + 6000 )) --scale 2 &
  sleep 2
  PORT=$(( $i + 6000 )) python3 student.py &
done