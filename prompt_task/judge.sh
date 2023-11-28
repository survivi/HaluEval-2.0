#!/bin/bash

ModelList=("chatgpt" "llama-2-7b-chat-hf")
DirList=("base" "character_info" "domain_info" "generate_demo" "pos_behind" "search_demo" "wrong_demo")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        nohup python -u judge.py --all-files --model $model --data-dir "./fact/prompt_format/$dir/$model/" --save-dir "./judge/prompt_format/$dir/$model/" >> ./judge_log/prompt_format_judge_$dir\_$model.log 2>&1 &
    done
done

ModelList2=("chatgpt" "llama-2-7b-chat-hf")
DirList2=("0-shot-cot" "few-shot-cot" "refine-q")
for model in ${ModelList2[*]}; do
    for dir in ${DirList2[*]}; do
        nohup python -u judge.py --all-files --model $model --data-dir "./fact/prompt_improvement/$dir/$model/" --save-dir "./judge/prompt_improvement/$dir/$model/" >> ./judge_log/prompt_improvement_judge_$dir\_$model.log 2>&1 &
    done
done

nohup python -u judge.py --all-files --model llama-2-7b-chat-hf --data-dir "./fact/self_reflexion/7b/" --save-dir "./judge/self_reflexion/7b/" >> ./judge_log/self_reflexion_7b_judge.log 2>&1 &
nohup python -u judge.py --all-files --model llama-2-13b-chat-hf --data-dir "./fact/self_reflexion/13b/" --save-dir "./judge/self_reflexion/13b/" >> ./judge_log/self_reflexion_13b_judge.log 2>&1 &
nohup python -u judge.py --all-files --model llama-2-70b-chat-hf --data-dir "./fact/self_reflexion/70b/" --save-dir "./judge/self_reflexion/70b/" >> ./judge_log/self_reflexion_70b_judge.log 2>&1 &
nohup python -u judge.py --all-files --model llama-2-70b-chat-hf --data-dir "./fact/self_reflexion/70b_raw/" --save-dir "./judge/self_reflexion/70b_raw/" >> ./judge_log/self_reflexion_70b_raw_judge.log 2>&1 &
