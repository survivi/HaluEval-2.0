#!/bin/bash
export OPENAI_API_KEY="sk-CSw9knewT4AnOU9C21Fa655bEfA44e8591D7932e59632c7f"
export OPENAI_API_BASE="https://api.aiguoguo199.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"
python main.py --all-files --model chatgpt --data-dir ./annotation/query/ --save-dir ./response/chatgpt_greedy/ --temperature 0