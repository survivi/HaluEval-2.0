#!/bin/bash

ModelList=("llama-2-7b-chat-hf")
DirList=("0-shot-cot" "few-shot-cot" "refine-q" "human_detailed" "model_detailed")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        nohup python -u judge.py --all-files --model $model --data-dir "./fact/prompt_improvement/$dir/$model/" --save-dir "./prompt_judge/prompt_improvement/$dir/$model/" >> ./judge_log/prompt_improvement_judge_$dir\_$model.log 2>&1 &
    done
done
