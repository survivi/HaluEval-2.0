#!/bin/bash
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 1.0 --data-dir ./annotation/query/ --save-dir ./response/llama-2-7b-chat-hf_top-p_10/