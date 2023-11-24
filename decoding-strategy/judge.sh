#!/bin/bash

DirList=("chatgpt_greedy" "chatgpt_top-p" "llama-2-7b-chat-hf_beam" "llama-2-7b-chat-hf_top-k" "llama-2-7b-chat-hf_top-p" "llama-2-7b-chat-hf_top-p_2" "llama-2-7b-chat-hf_top-p_4" "llama-2-7b-chat-hf_top-p_6" "llama-2-7b-chat-hf_top-p_8" "llama-2-7b-chat-hf_top-p_10")

for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u judge.py --all-files --model $model --assist-model gpt-4 --data-dir "./fact/$dir" --save-dir "./judge/$dir" >> ./log/judge_$dir.log 2>&1 &
done
