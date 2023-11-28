#!/bin/bash

ModelList=("chatgpt" "llama-2-7b-chat-hf")
DirList=("base" "character_info" "domain_info" "generate_demo" "pos_behind" "search_demo" "wrong_demo")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir "./prompt_data/prompt_format/$dir/$model/" --save-dir "./fact/prompt_format/$dir/$model/" >> ./fact_log/prompt_format_fact_$dir\_$model.log 2>&1 &
    done
done

ModelList2=("chatgpt" "llama-2-7b-chat-hf")
DirList2=("0-shot-cot" "few-shot-cot" "refine-q")
for model in ${ModelList2[*]}; do
    for dir in ${DirList2[*]}; do
        nohup python -u fact.py --all-files --model $model --data-dir "./prompt_data/prompt_improvement/$dir/$model/" --save-dir "./fact/prompt_improvement/$dir/$model/" >> ./fact_log/prompt_improvement_fact_$dir\_$model.log 2>&1 &
    done
done

nohup python -u fact.py --all-files --model llama-2-7b-chat-hf --data-dir "./prompt_data/self_reflexion/7b/" --save-dir "./fact/self_reflexion/7b/" >> ./fact_log/self_reflexion_7b_fact.log 2>&1 &
nohup python -u fact.py --all-files --model llama-2-13b-chat-hf --data-dir "./prompt_data/self_reflexion/13b/" --save-dir "./fact/self_reflexion/13b/" >> ./fact_log/self_reflexion_13b_fact.log 2>&1 &
nohup python -u fact.py --all-files --model llama-2-70b-chat-hf --data-dir "./prompt_data/self_reflexion/70b/" --save-dir "./fact/self_reflexion/70b/" >> ./fact_log/self_reflexion_70b_fact.log 2>&1 &
nohup python -u fact.py --all-files --model llama-2-70b-chat-hf --data-dir "./prompt_data/self_reflexion/70b_raw/" --save-dir "./fact/self_reflexion/70b_raw/" >> ./fact_log/self_reflexion_70b_raw_fact.log 2>&1 &
