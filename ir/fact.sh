#!/bin/bash

export OPENAI_API_KEY="sk-oLf6htFGHwu9Hc1ABb5eCe82E7C34b9e84A9D9Ef1bF472E5"
export OPENAI_API_BASE="https://api.pumpkinaigc.online/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

DirList=("response-1" "response-50" "response-100")
# ModelList=("chatgpt" "text-davinci-002" "text-davinci-003" "llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "alpaca-7b" "vicuna-7b" "vicuna-13b" "claude-1" "claude-2")
ModelList=("chatgpt" "llama-2-7b-chat-hf")
for dir in ${DirList[*]}; do
    for model in ${ModelList[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir ./ir_response_pure/$dir/$model --save-dir ./fact/$dir/$model >> ./log/fact_$dir\_$model.log 2>&1 &
    done
done
