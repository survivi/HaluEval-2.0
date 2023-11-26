#!/bin/bash

DirList=("llama-2-7b-chat-hf_INT4" "llama-2-7b-chat-hf_INT8" "llama-2-13b-chat-hf_INT4" "llama-2-13b-chat-hf_INT8")

for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u judge.py --all-files --model $model --assist-model gpt-4 --data-dir "./fact/$dir" --save-dir "./judge/$dir" >> ./judge_log/quantization_judge_$dir.log 2>&1 &
done

nohup python -u judge.py --all-files --model llama-7b --assist-model gpt-4 --data-dir "./fact/llama-7b/" --save-dir "./judge/llama-7b/" >> ./judge_log/judge_llama-7b.log 2>&1 &

nohup python -u judge.py --all-files --model claude-1 --assist-model gpt-4 --data-dir "./fact/claude-1/" --save-dir "./judge/claude-1/" >> ./judge_log/judge_claude-1.log 2>&1 &

nohup python -u judge.py --all-files --model claude-2 --assist-model gpt-4 --data-dir "./fact/claude-2/" --save-dir "./judge/claude-2/" >> ./judge_log/judge_claude-2.log 2>&1 &

DirList2=("complexity" "difficulty" "diversity" "scaling")

for dir in ${DirList2[*]}; do
    nohup python -u judge.py --all-files --model llama-7b --assist-model gpt-4 --data-dir "./fact/$dir" --save-dir "./judge/$dir" >> ./judge_log/sft_judge_$dir.log 2>&1 &
done
