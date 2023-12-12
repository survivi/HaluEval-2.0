#!/bin/bash

export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model llama-2-70b-chat-hf --data-dir ./annotation/query/ >> llama-2-70b-chat-hf.log 2>&1 &
