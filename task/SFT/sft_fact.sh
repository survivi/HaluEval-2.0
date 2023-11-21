#!/bin/bash

DirList=("complexity" "difficulty" "diversity" "scaling")

for dir in ${DirList[*]}; do
    nohup python -u fact.py --all-files --model llama-7b --data-dir "./sft_data/$dir" --save-dir "./fact/$dir" >> ./log/sft_fact_$dir.log 2>&1 &
done
