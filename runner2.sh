#!/bin/bash
rm results.txt
touch results.txt
tries=10
sum=0
for (( counter=$tries; counter>0; counter-- ))
do
python3 student.py
done

python3 avg.py
cat results.txt