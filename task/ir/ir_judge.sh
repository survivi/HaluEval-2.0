#!/bin/bash

export OPENAI_API_KEY="sk-uQgp6DoH8VpwMphgC44e7f04DdA24f37B5A6C2B899A9F040"
export OPENAI_API_BASE="https://api.chatgpt-3.vip/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

DirList=("response-1" "response-10" "response-50" "response-100")
ModelList=("chatgpt" "llama-2-7b-chat-hf")
for dir in ${DirList[*]}; do
    for model in ${ModelList[*]}; do
        nohup python -u judge.py --all-files --model $model --data-dir ./fact/$dir/$model --save-dir ./ir_response_judge/$dir/$model >> ./log/judge_$dir\_$model.log 2>&1 &
    done
done
