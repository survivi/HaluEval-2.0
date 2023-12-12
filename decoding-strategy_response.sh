#!/bin/bash

# chatgpt top-p
export OPENAI_API_KEY="sk-zlj8Kkvc7FNNdiyb3bA7F06eBc9345339e0f59A81b5e8f34"
export OPENAI_API_BASE="https://api.aiguoguo199.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

nohup python -u response.py --all-files --model chatgpt --top-p 0.2 --temperature 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/chatgpt_top-p_2/ >> ./log/chatgpt_top-p_2.log 2>&1 &
nohup python -u response.py --all-files --model chatgpt --top-p 0.4 --temperature 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/chatgpt_top-p_4/ >> ./log/chatgpt_top-p_4.log 2>&1 &
nohup python -u response.py --all-files --model chatgpt --top-p 0.6 --temperature 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/chatgpt_top-p_6/ >> ./log/chatgpt_top-p_6.log 2>&1 &
nohup python -u response.py --all-files --model chatgpt --top-p 0.8 --temperature 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/chatgpt_top-p_8/ >> ./log/chatgpt_top-p_8.log 2>&1 &
nohup python -u response.py --all-files --model chatgpt --top-p 1.0 --temperature 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/chatgpt_top-p_10/ >> ./log/chatgpt_top-p_10.log 2>&1 &
