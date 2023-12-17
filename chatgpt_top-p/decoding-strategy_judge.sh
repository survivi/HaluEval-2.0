#!/bin/bash

DirList=("chatgpt_top-p_2" "chatgpt_top-p_4" "chatgpt_top-p_6" "chatgpt_top-p_8" "chatgpt_top-p_10")

for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u judge.py --all-files --model $model --data-dir "./fact/$dir" --save-dir "./judge/$dir" >> ./log/decoding-strategy_judge_$dir.log 2>&1 &
done
