#!/bin/bash

# ModelList=("chatgpt" "text-davinci-002" "text-davinci-003" "llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "alpaca-7b" "vicuna-7b" "vicuna-13b" "claude-1" "claude-2")
# for model in ${ModelList[*]}; do
#     python metric.py --model $model --data-dir "./task/main/judge/$model"
# done

# DirList=("complexity" "difficulty" "diversity" "scaling")
# for dir in ${DirList[*]}; do
#     python metric.py --model llama-7b --data-dir "./task/SFT/sft_judge/$dir"
# done
# python metric.py --model llama-7b --data-dir "./task/SFT/sft_judge/llama-7b/"


# DirList=("chatgpt_greedy" "chatgpt_top-p" "llama-2-7b-chat-hf_beam" "llama-2-7b-chat-hf_top-k" "llama-2-7b-chat-hf_top-p" "llama-2-7b-chat-hf_greedy")
# for dir in ${DirList[*]}; do
#     model=${dir%%_*}
#     python metric.py --model $model --data-dir "./task/decoding-strategy/decoding-strategy_judge/$dir"
# done


# DirList=("llama-2-7b-chat-hf_top-p_2" "llama-2-7b-chat-hf_top-p_4" "llama-2-7b-chat-hf_top-p_6" "llama-2-7b-chat-hf_top-p_8" "llama-2-7b-chat-hf_top-p_10")
# for dir in ${DirList[*]}; do
#     model=${dir%%_*}
#     python metric.py --model $model --data-dir "./task/decoding-strategy/decoding-strategy_judge/$dir"
# done


# ModelList=("baichuan2-7b-intermediate-00220" "baichuan2-7b-intermediate-00440" "baichuan2-7b-intermediate-00660" "baichuan2-7b-intermediate-00880" "baichuan2-7b-intermediate-01100" "baichuan2-7b-intermediate-01320" "baichuan2-7b-intermediate-01540" "baichuan2-7b-intermediate-01760" "baichuan2-7b-intermediate-01980" "baichuan2-7b-intermediate-02200" "baichuan2-7b-intermediate-02420")
# for model in ${ModelList[*]}; do
#     python metric.py --model $model --data-dir "./task/pretrain/baichuan_judge/$model"
# done

# python metric.py --model yulan-chat-2-13b-fp16 --data-dir "./task/main/judge/yulan-chat-2-13b-fp16"

# DirList=("base" "character_info" "domain_info" "generate_demo" "pos_behind" "search_demo" "wrong_demo")
# for dir in ${DirList[*]}; do
#     python metric.py --model chatgpt --data-dir "./task/prompt_task/prompt_judge/prompt_format/$dir/chatgpt"
# done
# for dir in ${DirList[*]}; do
#     python metric.py --model llama-2-7b-chat-hf --data-dir "./task/prompt_task/prompt_judge/prompt_format/$dir/llama-2-7b-chat-hf"
# done

# DirList=("llama-2-7b-chat-hf_INT4" "llama-2-7b-chat-hf_INT8" "llama-2-13b-chat-hf_INT4" "llama-2-13b-chat-hf_INT8")
# for dir in ${DirList[*]}; do
#     model=${dir%%_*}
#     python metric.py --model $model --data-dir "./task/quantization/quantization_judge/$dir"
# done

# DirList=("llama-2-7b-chat-hf" "llama-2-13b-chat-hf")
# for dir in ${DirList[*]}; do
#     python metric.py --model $dir --data-dir "./task/prompt_task/prompt_judge/origin/$dir"
# done

# ModelList=("yulan-chat-2-13b-fp16")
# for model in ${ModelList[*]}; do
#     python metric.py --model $model --data-dir "./task/main/judge/$model"
# done

DirList=("chatgpt_top-p_2" "chatgpt_top-p_4" "chatgpt_top-p_6" "chatgpt_top-p_8" "chatgpt_top-p_10")
for dir in ${DirList[*]}; do
    model=${dir%%_*}
    python metric.py --model $model --data-dir "./chatgpt_top-p/judge/$dir"
done
