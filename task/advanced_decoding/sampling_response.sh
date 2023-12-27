#!/bin/bash

nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.5 --data-dir ./annotation/query/ --save-dir ./gns_response/ > gns.log 2>&1 &

nohup python -u response.py --all-files --model llama-2-7b-chat-hf --do-sample --top-k 0 --top-p 0.9 --data-dir ./annotation/query/ --save-dir ./fns_response/ > fns.log 2>&1 &
