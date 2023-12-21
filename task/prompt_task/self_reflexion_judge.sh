#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

nohup python -u judge.py --all-files --model llama-2-7b-chat-hf --data-dir "./fact/self_reflexion/llama-2-7b-chat-hf/" --save-dir "./prompt_judge/self_reflexion/llama-2-7b-chat-hf/" >> ./judge_log/self_reflexion_7b_judge.log 2>&1 &
nohup python -u judge.py --all-files --model llama-2-13b-chat-hf --data-dir "./fact/self_reflexion/llama-2-13b-chat-hf/" --save-dir "./prompt_judge/self_reflexion/llama-2-13b-chat-hf/" >> ./judge_log/self_reflexion_13b_judge.log 2>&1 &
nohup python -u judge.py --all-files --model llama-2-70b-chat-hf --data-dir "./fact/self_reflexion/llama-2-70b-chat-hf/" --save-dir "./prompt_judge/self_reflexion/llama-2-70b-chat-hf/" >> ./judge_log/self_reflexion_70b_judge.log 2>&1 &
