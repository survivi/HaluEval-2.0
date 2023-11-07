#!/bin/bash
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 50 --save-dir ./response/llama-2-7b-chat-hf_top-k/