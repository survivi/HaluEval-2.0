#!/bin/bash

DirList=("chatgpt_greedy" "chatgpt_top-p" "llama-2-7b-chat-hf_beam" "llama-2-7b-chat-hf_top-k" "llama-2-7b-chat-hf_top-p" "llama-2-7b-chat-hf_top-p_2" "llama-2-7b-chat-hf_top-p_4" "llama-2-7b-chat-hf_top-p_6" "llama-2-7b-chat-hf_top-p_8" "llama-2-7b-chat-hf_top-p_10")

for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u fact.py --all-files --model $model --assist-model gpt-4 --data-dir "./decoding-strategy_data/$dir" --save-dir "./fact/$dir" >> ./log/fact_$dir.log 2>&1 &
done
