#!/bin/bash
# ModelList=("chatgpt" "text-davinci-002" "text-davinci-003" "llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "alpaca-7b" "vicuna-7b" "vicuna-13b" "claude-1" "claude-2")
# for model in ${ModelList[*]}; do
#     python metric.py --model $model --data-dir "./task/main/judge/$model"
# done

# DirList=("chatgpt_greedy" "chatgpt_top-p" "llama-2-7b-chat-hf_beam" "llama-2-7b-chat-hf_top-k" "llama-2-7b-chat-hf_top-p" "llama-2-7b-chat-hf_top-p_2" "llama-2-7b-chat-hf_top-p_4" "llama-2-7b-chat-hf_top-p_6" "llama-2-7b-chat-hf_top-p_8" "llama-2-7b-chat-hf_top-p_10")

# for dir in ${DirList[*]}; do
#     model=${dir%%_*}
#     python metric.py --model $model --data-dir "./task/decoding-strategy/decoding-strategy_judge/$dir"
# done

DirList=("complexity" "difficulty" "diversity" "scaling")

for dir in ${DirList[*]}; do
    python metric.py --model llama-7b --data-dir "./task/SFT/sft_judge/$dir"
done

python metric.py --model llama-7b --data-dir "./task/SFT/sft_judge/llama-7b/"
