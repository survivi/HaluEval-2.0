#!/bin/bash

DirList=("response-1" "response-50" "response-100")
ModelList=("chatgpt" "text-davinci-002" "text-davinci-003" "llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "alpaca-7b" "vicuna-7b" "vicuna-13b" "claude-1" "claude-2")
for dir in ${DirList[*]}; do
    for model in ${ModelList[*]}; do
        nohup python -u judge.py --all-files --model $model --data-dir ./fact/$dir/$model --save-dir ./judge/$dir/$model >> ./log/judge_$dir\_$model.log 2>&1 &
    done
done
