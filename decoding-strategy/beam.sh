#!/bin/bash
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-2-7b-chat-hf --num-beams 5 --early-stopping --save-dir ./response/llama-2-7b-chat-hf_beam/