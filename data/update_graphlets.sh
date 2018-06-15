#!/bin/bash

for g in ./graphs/*; 
do
  ../e_clog/omp_graphlet_count_5 -i $g > log.txt
  filename=$(basename $g)
  filename="${filename%.*}"
  mv $g"_local_graphlet_freqeuncy_5_omp.txt" "graphlets/"$filename".gfc"
  echo $filename
done
