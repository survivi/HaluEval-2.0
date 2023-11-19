# #!/bin/bash

# llama-2-7b-chat-hf top-p 0.5
export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.5 --data-dir ./annotation/query/ --save-dir ./task/decoding-strategy/decoding-strategy_data/llama-2-7b-chat-hf_top-p/ >> llama-2-7b-chat_top-p.log 2>&1 &
