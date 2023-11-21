#!/bin/bash

DirList=("llama-2-7b-chat-hf_INT4" "llama-2-7b-chat-hf_INT8" "llama-2-13b-chat-hf_INT4" "llama-2-13b-chat-hf_INT8")

for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u judge.py --all-files --model $model --data-dir "./fact/$dir" --save-dir "./judge/$dir" >> ./log/quantization_judge_$dir.log 2>&1 &
done
