#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
python main.py --all-files --model llama-2-7b-chat-hf
export CUDA_VISIBLE_DEVICES=gpu_id1 && CUDA_VISIBLE_DEVICES=gpu_id2 python3 train.py