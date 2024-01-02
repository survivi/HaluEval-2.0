#!/bin/bash

DirList=("response_1docs_top1" "response_5docs_top5" "response_10docs_top10" "response_1docs_top2" "response_1docs_top5" "response_1docs_top10")
ModelList=("chatgpt" "llama-2-7b-chat-hf")
for dir in ${DirList[*]}; do
    for model in ${ModelList[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir ./ir_response_pure/$dir/$model --save-dir ./fact/$dir/$model > ./fact_log/fact_$dir\_$model.log 2>&1 &
    done
done

DirList=("response_2docs_top2")
ModelList=("chatgpt" "llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "vicuna-7b" "vicuna-13b")
for dir in ${DirList[*]}; do
    for model in ${ModelList[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir ./ir_response_pure/$dir/$model --save-dir ./fact/$dir/$model > ./fact_log/fact_$dir\_$model.log 2>&1 &
    done
done
