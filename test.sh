#!/bin/bash

export CUDA_VISIBLE_DEVICES=1 && nohup python -u test.py --file Bio-Medical --model llama-2-70b-hf --data-dir "./data/" --save-dir "./temp/" >> ./test.log 2>&1 &
