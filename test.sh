#!/bin/bash

export CUDA_VISIBLE_DEVICES=8 && nohup python -u test.py --file Bio-Medical --model llama-2-7b-hf --data-dir "./data/" --save-dir "./temp/" >> test.log 2>&1 &

export CUDA_VISIBLE_DEVICES=9 && nohup python -u test_half.py --file Bio-Medical --model llama-2-7b-hf --data-dir "./data/" --save-dir "./temp/" >> test_half.log 2>&1 &
