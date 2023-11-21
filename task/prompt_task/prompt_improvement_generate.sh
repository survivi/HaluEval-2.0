#!/bin/bash

ModelList=("chatgpt" "llama-2-7b-chat-hf")
DirList=("0-shot-cot" "few-shot-cot" "refine-q")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir "./prompt_data/prompt_improvement/$dir/$model/" --save-dir "./fact/prompt_improvement/$dir/$model/" >> ./log/prompt_improvement_fact_$dir\_$model.log 2>&1 &
    done
done
