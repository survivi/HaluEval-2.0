#!/bin/bash

ModelList=("yulan-chat-2-13b-fp16")
for model in ${ModelList[*]}; do
    nohup python -u fact.py --all-files --model $model >> ./log/fact_$model.log 2>&1 &
done
