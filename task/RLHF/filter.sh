#!/bin/bash

for model in alpaca-7b vicuna-7b vicuna-13b
do
    nohup python -u rlhf_filter.py --model $model --all-files > ./log/filter_$model.log 2>&1 &
done
