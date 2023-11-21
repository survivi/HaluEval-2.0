#!/bin/bash
nohup python -u judge.py --all-files --model llama-7b --data-dir "./fact/llama-7b/" --save-dir "./judge/llama-7b/">> ./log/judge_llama-7b.log 2>&1 &
