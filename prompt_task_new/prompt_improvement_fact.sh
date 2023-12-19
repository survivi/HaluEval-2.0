#!/bin/bash

export OPENAI_API_KEY="sk-sfZjeU96BRSkTorJ5083FaD2Eb804c3fB7C623AcCf2dEbF3"
export OPENAI_API_BASE="https://api.chatgpt-3.vip/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

ModelList=("llama-2-7b-chat-hf")
DirList=("0-shot-cot" "few-shot-cot" "refine-q" "human_detailed" "model_detailed")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir "./prompt_response/prompt_improvement/$dir/$model/" --save-dir "./fact/prompt_improvement/$dir/$model/" >> ./fact_log/prompt_improvement_fact_$dir\_$model.log 2>&1 &
    done
done
