#!/bin/bash

export OPENAI_API_KEY="sk-48yzfFzhe1ACttDc3569Dc105dF3467b92AcD19cD4534c9d"
export OPENAI_API_BASE="https://ngapi.fun/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

for model in alpaca-7b vicuna-7b vicuna-13b
do
    nohup python -u rlhf_generate.py --model $model --all-files >> ./log/gen_$model.log 2>&1 &
done
