#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

nohup python -u fact.py --all-files --model llama-7b --data-dir "./sft_response/llama-7b/" --save-dir "./fact/llama-7b/" >> ./log/sft_fact_llama-7b.log 2>&1 &

DirList=("complexity" "difficulty" "diversity" "scaling")
for dir in ${DirList[*]}; do
    nohup python -u fact.py --all-files --model llama-7b --data-dir "./sft_response/$dir" --save-dir "./fact/$dir" >> ./log/sft_fact_$dir.log 2>&1 &
done

DirList=("flan" "sharegpt" "sinstruct" "sinstruct_sharegpt" "sinstruct_sharegpt_flan_10k")
for dir in ${DirList[*]}; do
    nohup python -u fact.py --all-files --model llama-7b --data-dir "./sft_response/$dir" --save-dir "./fact/$dir" >> ./log/sft_fact_$dir.log 2>&1 &
done
