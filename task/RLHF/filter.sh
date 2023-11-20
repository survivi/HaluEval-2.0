#!/bin/bash
for model in alpaca-7b vicuna-7b vicuna-13b
do
    for file in Bio-Medical Finance Science Education Open-Domain
    do
        nohup python -u rlhf_filter.py --model $model --file $file >> filter_$model\_$file.log 2>&1 &
    done
done
