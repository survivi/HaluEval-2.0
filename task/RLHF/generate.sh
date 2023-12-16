#!/bin/bash

# for model in alpaca-7b vicuna-7b vicuna-13b
# do
#     nohup python -u rlhf_generate.py --model $model --all-files >> ./log/gen_$model.log 2>&1 &
# done

export OPENAI_API_KEY="sk-qDgYyI6GmsyFvhhd1c6d9c8127Ea4b5aA4E66aC856E404E0"
export OPENAI_API_BASE="https://ngapi.fun/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

for model in alpaca-7b
do
    nohup python -u rlhf_generate.py --model $model --file Bio-Medical >> ./log/gen_$model.log 2>&1 &
done
