#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

nohup python -u fact.py --all-files --model llama-7b --data-dir "./llama-7b/" --save-dir "./fact/llama-7b/" >> ./log/fact_llama-7b.log 2>&1 &
