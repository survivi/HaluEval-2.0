#!/bin/bash

DirList=("llama-2-7b-chat-hf_INT4" "llama-2-7b-chat-hf_INT8" "llama-2-13b-chat-hf_INT4" "llama-2-13b-chat-hf_INT8")

for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u fact.py --all-files --model $model --assist-model gpt-4 --data-dir "./quantization_data/$dir" --save-dir "./fact/$dir" >> ./fact_log/quantization_fact_$dir.log 2>&1 &
done

nohup python -u fact.py --all-files --model llama-7b --assist-model gpt-4 --data-dir "./llama-7b/" --save-dir "./fact/llama-7b/" >> ./fact_log/fact_llama-7b.log 2>&1 &

nohup python -u fact.py --all-files --model claude-1 --assist-model gpt-4 --data-dir "./claude-1/" --save-dir "./fact/claude-1/" >> ./fact_log/fact_claude-1.log 2>&1 &

nohup python -u fact.py --all-files --model claude-2 --assist-model gpt-4 --data-dir "./claude-2/" --save-dir "./fact/claude-2/" >> ./fact_log/fact_claude-2.log 2>&1 &

DirList2=("complexity" "difficulty" "diversity" "scaling")

for dir in ${DirList2[*]}; do
    nohup python -u fact.py --all-files --model llama-7b --assist-model gpt-4 --data-dir "./sft_data/$dir" --save-dir "./fact/$dir" >> ./fact_log/sft_fact_$dir.log 2>&1 &
done
