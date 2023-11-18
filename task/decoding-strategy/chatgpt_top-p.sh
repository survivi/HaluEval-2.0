#!/bin/bash
export OPENAI_API_KEY="sk-itJLSDtI0l1xEngiAf5c0b742f48475185901cB90aB9D68a"
export OPENAI_API_BASE="https://api.aiguoguo199.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"
python main.py --all-files --model chatgpt --data-dir ./annotation/query/ --save-dir ./response/chatgpt_top-p/ --top-p 0.5 --temperature 1