#!/bin/bash

# export OPENAI_API_KEY="sk-"
# export OPENAI_API_BASE="https://api.openai.com/v1"
# echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
# echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

ModelList=("chatgpt" "llama-2-7b-chat-hf")
DirList=("0-shot-cot" "few-shot-cot" "refine-q" "human_detailed" "model_detailed")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        nohup python -u judge.py --all-files --model $model --data-dir "./fact/prompt_improvement/$dir/$model/" --save-dir "./prompt_judge/prompt_improvement/$dir/$model/" >> ./judge_log/prompt_improvement_judge_$dir\_$model.log 2>&1 &
    done
done
