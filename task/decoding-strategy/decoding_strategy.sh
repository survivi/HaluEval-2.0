#!/bin/bash

# chatgpt greedy
export OPENAI_API_KEY="sk-CSw9knewT4AnOU9C21Fa655bEfA44e8591D7932e59632c7f"
export OPENAI_API_BASE="https://api.aiguoguo199.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"
nohup python -u response.py --all-files --model chatgpt  --temperature 0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/chatgpt_greedy/ >> chatgpt_greedy.log 2>&1 &

# chatgpt top-p 0.5
export OPENAI_API_KEY="sk-itJLSDtI0l1xEngiAf5c0b742f48475185901cB90aB9D68a"
export OPENAI_API_BASE="https://api.aiguoguo199.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"
nohup python -u response.py --all-files --model chatgpt --top-p 0.5 --temperature 1 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/chatgpt_top-p/ >> chatgpt_top-p.log 2>&1 &

# llama-2-7b-chat-hf beam search
export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model llama-2-7b-chat-hf --num-beams 5 --early-stopping --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/llama-2-7b-chat-hf_beam/ >> llama-2-7b-chat_beam.log 2>&1 &

# llama-2-7b-chat-hf top-k 50
export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 50 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/llama-2-7b-chat-hf_top-k/ >> llama-2-7b-chat_top-k.log 2>&1 &

# llama-2-7b-chat-hf top-p 0.5
export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.5 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/llama-2-7b-chat-hf_top-p/ >> llama-2-7b-chat_top-p.log 2>&1 &

# llama-2-7b-chat-hf top-p 0.2
export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.2 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/llama-2-7b-chat-hf_top-p_2/ >> llama-2-7b-chat_top-p_2.log 2>&1 &

# llama-2-7b-chat-hf top-p 0.4
export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.4 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/llama-2-7b-chat-hf_top-p_4/ >> llama-2-7b-chat_top-p_4.log 2>&1 &

# llama-2-7b-chat-hf top-p 0.6
export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.6 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/llama-2-7b-chat-hf_top-p_6/ >> llama-2-7b-chat_top-p_6.log 2>&1 &

# llama-2-7b-chat-hf top-p 0.8
export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.8 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/llama-2-7b-chat-hf_top-p_8/ >> llama-2-7b-chat_top-p_8.log 2>&1 &

# llama-2-7b-chat-hf top-p 1.0
export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 1.0 --data-dir ./annotation/query/ --save-dir ./decoding-strategy_data/llama-2-7b-chat-hf_top-p_10/ >> llama-2-7b-chat_top-p_10.log 2>&1 &
