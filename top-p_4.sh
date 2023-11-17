#!/bin/bash
export CUDA_VISIBLE_DEVICES=3
python main.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.4 --data-dir "./annotation/query/" --save-dir ./response/llama-2-7b-chat-hf_top-p_4/