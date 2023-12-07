#!/bin/bash

ModelList=("yulan-chat-2-13b-fp16")
for model in ${ModelList[*]}; do
    nohup python -u judge.py --all-files --model $model >> ./log/judge_$model.log 2>&1 &
done
