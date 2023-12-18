#!/bin/bash

DirList=("flan" "sharegpt" "sinstruct" "sinstruct_sharegpt" "sinstruct_sharegpt_flan_10k")

for dir in ${DirList[*]}; do
    nohup python -u fact.py --all-files --model llama-7b --data-dir "./sft2/$dir" --save-dir "./fact/$dir" >> ./log/sft_fact_$dir.log 2>&1 &
done