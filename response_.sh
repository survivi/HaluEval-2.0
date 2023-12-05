#!/bin/bash

export CUDA_VISIBLE_DEVICES=9 && nohup python -u response.py --all-files --model yulan-chat-2-13b-fp16 >> ./log/yulan.log 2>&1 &
