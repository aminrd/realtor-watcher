#! /bin/bash

x=1
while [ $x -le 5 ]
do
  python watch.py --verbose True --links links.csv --update_file updates.txt
  sleep 12h
done