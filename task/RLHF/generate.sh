#!/bin/bash

for model in alpaca-7b vicuna-7b vicuna-13b
do
    nohup python -u rlhf_generate.py --model $model --all-files >> ./log/gen_$model.log 2>&1 &
done
