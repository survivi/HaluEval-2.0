#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

DirList=("llama-2-7b-chat-hf_INT4" "llama-2-7b-chat-hf_INT8" "llama-2-13b-chat-hf_INT4" "llama-2-13b-chat-hf_INT8")
for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u judge.py --all-files --model $model --data-dir "./fact/$dir" --save-dir "./judge/$dir" >> ./log/quantization_judge_$dir.log 2>&1 &
done
