#!/bin/bash

DirList=("chatgpt_top-p_2" "chatgpt_top-p_4" "chatgpt_top-p_6" "chatgpt_top-p_8" "chatgpt_top-p_10")

for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u fact.py --all-files --model $model --data-dir "./decoding-strategy_data/$dir" --save-dir "./fact/$dir" >> ./log/decoding-strategy_fact_$dir.log 2>&1 &
done
