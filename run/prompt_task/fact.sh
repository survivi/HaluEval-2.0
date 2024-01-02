#!/bin/bash

export OPENAI_API_KEY="sk-vo6dWBfoLsXQW7bh213190177a8b4e489f83Ea18F63a7aF6"
export OPENAI_API_BASE="https://api.chatgpt-3.vip/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

ModelList=("chatgpt" "llama-2-7b-chat-hf")
DirList=("0-shot" "base" "character_info" "domain_info" "few-shot" "in-context_demo" "mannual_desc" "refine_q" "retrieved_demo" "reverse_pos" "synthetic_demo" "synthetic_desc" "wrong_demo")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir "./prompt_response_pure/$model/$dir" --save-dir "./fact/$model/$dir/" > ./fact_log/fact_$dir\_$model.log 2>&1 &
    done
done
