#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

# chatgpt greedy
nohup python -u response.py --all-files --model chatgpt  --temperature 0.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/chatgpt_greedy/ >> ./log/chatgpt_greedy.log 2>&1 &

# chatgpt top-p 0.5
nohup python -u response.py --all-files --model chatgpt --top-p 0.5 --temperature 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/chatgpt_top-p/ >> ./log/chatgpt_top-p.log 2>&1 &

# chatgpt top-p 0.2
nohup python -u response.py --all-files --model chatgpt --top-p 0.2 --temperature 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/chatgpt_top-p_2/ >> ./log/chatgpt_top-p_2.log 2>&1 &

# chatgpt top-p 0.4
nohup python -u response.py --all-files --model chatgpt --top-p 0.4 --temperature 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/chatgpt_top-p_4/ >> ./log/chatgpt_top-p_4.log 2>&1 &

# chatgpt top-p 0.6
nohup python -u response.py --all-files --model chatgpt --top-p 0.6 --temperature 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/chatgpt_top-p_6/ >> ./log/chatgpt_top-p_6.log 2>&1 &

# chatgpt top-p 0.8
nohup python -u response.py --all-files --model chatgpt --top-p 0.8 --temperature 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/chatgpt_top-p_8/ >> ./log/chatgpt_top-p_8.log 2>&1 &

# chatgpt top-p 1.0
nohup python -u response.py --all-files --model chatgpt --top-p 1.0 --temperature 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/chatgpt_top-p_10/ >> ./log/chatgpt_top-p_10.log 2>&1 &

# llama-2-7b-chat-hf beam search
nohup python -u response.py --all-files --model llama-2-7b-chat-hf --num-beams 5 --early-stopping --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/llama-2-7b-chat-hf_beam/ >> ./log/llama-2-7b-chat_beam.log 2>&1 &

# llama-2-7b-chat-hf top-k 50
nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 50 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/llama-2-7b-chat-hf_top-k/ >> ./log/llama-2-7b-chat_top-k.log 2>&1 &

# llama-2-7b-chat-hf top-p 0.5
nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.5 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/llama-2-7b-chat-hf_top-p/ >> ./log/llama-2-7b-chat_top-p.log 2>&1 &

# llama-2-7b-chat-hf top-p 0.2
nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.2 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/llama-2-7b-chat-hf_top-p_2/ >> ./log/llama-2-7b-chat_top-p_2.log 2>&1 &

# llama-2-7b-chat-hf top-p 0.4
nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.4 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/llama-2-7b-chat-hf_top-p_4/ >> ./log/llama-2-7b-chat_top-p_4.log 2>&1 &

# llama-2-7b-chat-hf top-p 0.6
nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.6 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/llama-2-7b-chat-hf_top-p_6/ >> ./log/llama-2-7b-chat_top-p_6.log 2>&1 &

# llama-2-7b-chat-hf top-p 0.8
nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.8 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/llama-2-7b-chat-hf_top-p_8/ >> ./log/llama-2-7b-chat_top-p_8.log 2>&1 &

# llama-2-7b-chat-hf top-p 1.0
nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_response/llama-2-7b-chat-hf_top-p_10/ >> ./log/llama-2-7b-chat_top-p_10.log 2>&1 &
