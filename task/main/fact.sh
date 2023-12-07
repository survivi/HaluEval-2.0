#!/bin/bash

ModelList=("chatgpt" "text-davinci-002" "text-davinci-003" "llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "alpaca-7b" "vicuna-7b" "vicuna-13b" "yulan-chat-2-13b-fp16")
for model in ${ModelList[*]}; do
    nohup python -u fact.py --all-files --model $model >> ./log/fact_$model.log 2>&1 &
done
