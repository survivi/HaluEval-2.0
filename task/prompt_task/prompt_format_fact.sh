#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

ModelList=("chatgpt" "llama-2-7b-chat-hf")
DirList=("base" "character_info" "domain_info" "generate_demo" "pos_behind" "search_demo" "wrong_demo")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir "./prompt_response/prompt_format/$dir/$model/" --save-dir "./fact/prompt_format/$dir/$model/" >> ./fact_log/prompt_format_fact_$dir\_$model.log 2>&1 &
    done
done
