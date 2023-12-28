#!/bin/bash

ModelList=("alpaca-7b" "vicuna-7b")
for model in ${ModelList[*]}; do
    nohup python -u fact.py --all-files --model $model >> ./log/fact_$model.log 2>&1 &
done
