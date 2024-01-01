#!/bin/bash

export OPENAI_API_KEY="sk-vo6dWBfoLsXQW7bh213190177a8b4e489f83Ea18F63a7aF6"
export OPENAI_API_BASE="https://api.chatgpt-3.vip/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

DirList=("response_1docs_top1" "response_2docs_top2" "response_5docs_top5" "response_10docs_top10")
ModelList=("chatgpt")
for dir in ${DirList[*]}; do
    for model in ${ModelList[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir ./ir_response_pure/$dir/$model --save-dir ./fact/$dir/$model > ./fact_$dir\_$model.log 2>&1 &
    done
done
