#!/bin/bash

DirList=("complexity" "difficulty" "diversity" "scaling")

for dir in ${DirList[*]}; do
    nohup python -u judge.py --all-files --model llama-7b --data-dir "./fact/$dir" --save-dir "./judge/$dir" >> ./log/sft_judge_$dir.log 2>&1 &
done

DirList=("flan" "sharegpt" "sinstruct" "sinstruct_sharegpt" "sinstruct_sharegpt_flan_10k")

for dir in ${DirList[*]}; do
    nohup python -u judge.py --all-files --model llama-7b --data-dir "./fact/$dir" --save-dir "./judge/$dir" >> ./log/sft_judge_$dir.log 2>&1 &
done
