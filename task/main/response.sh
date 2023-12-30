#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

nohup python -u response.py --all-files --model chatgpt --temperature 0 >> ./chatgpt.log 2>&1 &
nohup python -u response.py --all-files --model text-davinci-002 --temperature 0 >> ./text-davinci-002.log 2>&1 &
nohup python -u response.py --all-files --model text-davinci-003 --temperature 0 >> ./text-davinci-003.log 2>&1 &

ModelList=("llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "alpaca-7b" "vicuna-7b" "vicuna-13b" "yulan-chat-2-13b-fp16")
for model in ${ModelList[*]}; do
    nohup python -u response.py --all-files --model $model >> ./$model.log 2>&1 &
done
