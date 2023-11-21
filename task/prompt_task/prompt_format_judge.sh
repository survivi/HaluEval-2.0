#!/bin/bash

ModelList=("chatgpt" "llama-2-7b-chat-hf")
DirList=("base" "character_info" "domain_info" "generate_demo" "search_demo" "wrong_demo")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        nohup python -u judge.py --all-files --model $model --data-dir "./fact/prompt_format/$dir/$model/" --save-dir "./judge/prompt_format/$dir/$model/" >> ./log/prompt_format_judge_$dir\_$model.log 2>&1 &
    done
done
