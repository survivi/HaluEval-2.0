#!/bin/bash

export OPENAI_API_KEY="sk-GD2CUN4ZZoa4dEB1892e5eB187Df476eA04b4e9dC246E247"
export OPENAI_API_BASE="https://api.chatgpt-3.vip/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

DirList=("scaling")
for dir in ${DirList[*]}; do
    nohup python -u judge.py --all-files --model llama-7b --data-dir "./fact/$dir" --save-dir "./sft_judge/$dir" >> ./log/sft_judge_$dir.log 2>&1 &
done
