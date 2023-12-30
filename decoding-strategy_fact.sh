#!/bin/bash

export OPENAI_API_KEY="sk-q6avb9tefHRpXDoiF39069Ea2f92454b9aF6Da9c785a0eE1"
export OPENAI_API_BASE="https://api.chatgpt-3.vip/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

DirList=("vicuna-7b_greedy" "vicuna-13b_greedy")
for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u fact.py --all-files --model $model --data-dir "./task/decoding-strategy/decoding-strategy_response/$dir" --save-dir "./fact/$dir" >> ./decoding-strategy_fact_$dir.log 2>&1 &
done
