#!/bin/bash
export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model llama-7b --data-dir ./annotation/query/ --save-dir ./llama-7b/ >> ./log/llama-7b.log 2>&1 &
