#!/bin/bash

export OPENAI_API_KEY="sk-PrhJRQa8hh3QWoGcB9Ff11524e4b47A9B23169DaFd23D4D2"
export OPENAI_API_BASE="https://api.chatgpt-3.vip/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

DirList=("vicuna-7b_greedy" "vicuna-13b_greedy")
for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u fact.py --all-files --model $model --data-dir "./task/decoding-strategy/decoding-strategy_response/$dir" --save-dir "./fact/$dir" >> ./decoding-strategy_fact_$dir.log 2>&1 &
done
