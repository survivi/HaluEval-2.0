#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

DirList=("fns_response" "gns_response")
for dir in ${DirList[*]}; do
    nohup python -u judge.py --all-files --model llama-2-7b-chat-hf --data-dir ./fact/$dir --save-dir ./advanced_decoding_judge/$dir >> ./judge_$dir.log 2>&1 &
done