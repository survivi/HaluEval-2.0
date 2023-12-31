#!/bin/bash

export OPENAI_API_KEY="sk-PrhJRQa8hh3QWoGcB9Ff11524e4b47A9B23169DaFd23D4D2"
export OPENAI_API_BASE="https://api.chatgpt-3.vip/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

DirList=("alpaca-7b_greedy")
for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u judge.py --all-files --model $model --data-dir "./fact/$dir" --save-dir "./decoding-strategy_judge/$dir" >> ./decoding-strategy_judge_$dir.log 2>&1 &
done
