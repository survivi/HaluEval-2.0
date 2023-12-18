#!/bin/bash

export OPENAI_API_KEY="sk-vu2yPgLCrnFqq9AT823cEbF63d1249168bBd64A54a39A818"
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
