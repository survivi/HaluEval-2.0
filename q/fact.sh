#!/bin/bash

export OPENAI_API_KEY="sk-CSw9knewT4AnOU9C21Fa655bEfA44e8591D7932e59632c7f"
export OPENAI_API_BASE="https://api.aiguoguo199.com/v1"

DirList=("llama-2-7b-chat-hf_INT4" "llama-2-7b-chat-hf_INT8" "llama-2-13b-chat-hf_INT4" "llama-2-13b-chat-hf_INT8")

for dir in ${DirList[*]}; do
    model=${dir%%_*}
    nohup python -u fact.py --all-files --model $model --assist-model chatgpt --data-dir "./quantization_data/$dir" --save-dir "./fact/$dir" >> ./log/quantization_fact_$dir.log 2>&1 &
done

# nohup python -u fact.py --all-files --model llama-7b --data-dir "./llama-7b/" --save-dir "./fact/llama-7b/">> ./log/fact_llama-7b.log 2>&1 &
