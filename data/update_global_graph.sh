#!/bin/bash

for g in ./global_graphs/*; 
do
  echo $g
  ../guise/GUISE -d $g -i 2000 > log.txt
  
  filename=$(basename $g)
  filename="${filename%.*}"
  mv "graphlet_count" "global_graphlets/"$filename".gfc"
  echo $filename
done
