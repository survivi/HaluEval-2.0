#!/bin/bash

export OPENAI_API_KEY="sk-aRh0Y9eT5mJq4XY3D2E25c7545C3469386F47d815c9112F4"
export OPENAI_API_BASE="https://api.chatgpt-3.vip/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

DirList=("sinstruct")
for dir in ${DirList[*]}; do
    nohup python -u judge.py --all-files --model llama-7b --data-dir "./fact/$dir" --save-dir "./sft_judge/$dir" >> ./log/sft_judge_$dir.log 2>&1 &
done
