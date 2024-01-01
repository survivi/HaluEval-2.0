#!/bin/bash

export OPENAI_API_KEY="sk-vo6dWBfoLsXQW7bh213190177a8b4e489f83Ea18F63a7aF6"
export OPENAI_API_BASE="https://api.chatgpt-3.vip/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

ModelList=("alpaca-7b" "vicuna-7b")
for model in ${ModelList[*]}; do
    nohup python -u fact.py --all-files --model $model > ./log/fact_$model.log 2>&1 &
done
