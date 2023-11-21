#!/bin/bash
nohup python -u fact.py --all-files --model llama-7b --data-dir "./llama-7b/" --save-dir "./fact/llama-7b/">> ./log/fact_llama-7b.log 2>&1 &
