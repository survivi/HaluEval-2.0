#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

for model in alpaca-7b vicuna-7b vicuna-13b
do
    nohup python -u rlhf_generate.py --model $model --all-files >> ./log/gen_$model.log 2>&1 &
done
