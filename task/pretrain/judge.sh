#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

ModelList=("baichuan2-7b-intermediate-00220" "baichuan2-7b-intermediate-00440" "baichuan2-7b-intermediate-00660" "baichuan2-7b-intermediate-00880" "baichuan2-7b-intermediate-01100" "baichuan2-7b-intermediate-01320" "baichuan2-7b-intermediate-01540" "baichuan2-7b-intermediate-01760" "baichuan2-7b-intermediate-01980" "baichuan2-7b-intermediate-02200" "baichuan2-7b-intermediate-02420")
for model in ${ModelList[*]}; do
    nohup python -u judge.py --all-files --model $model >> ./judge_log/judge_$model.log 2>&1 &
done
