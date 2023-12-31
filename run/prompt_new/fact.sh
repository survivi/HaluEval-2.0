#!/bin/bash

# export OPENAI_API_KEY="sk-"
# export OPENAI_API_BASE="https://api.openai.com/v1"
# echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
# echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

ModelList=("chatgpt" "llama-2-7b-chat-hf")
DirList=("0-shot" "base" "character_info" "domain_info" "few-shot" "in-context_demo" "mannual_desc" "refine-q" "retrieved_demo" "reverse_pos" "synthetic_demo" "synthetic_desc" "wrong_demo")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir "./prompt_response_pure/$model/$dir" --save-dir "./fact/$model/$dir/" >> ./fact_log/fact_$dir\_$model.log 2>&1 &
    done
done
