#!/bin/bash

export OPENAI_API_KEY="sk-uQgp6DoH8VpwMphgC44e7f04DdA24f37B5A6C2B899A9F040"
export OPENAI_API_BASE="https://api.chatgpt-3.vip/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

# DirList=("response-1" "response-50" "response-100")
DirList=("response-10")
ModelList=("chatgpt" "llama-2-7b-chat-hf")
for dir in ${DirList[*]}; do
    for model in ${ModelList[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir ./ir_response_pure/$dir/$model --save-dir ./fact/$dir/$model >> ./log/fact_$dir\_$model.log 2>&1 &
    done
done
