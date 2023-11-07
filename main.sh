#!/bin/bash
export OPENAI_API_KEY="sk-AZFhjE7fZW33inqK0701D5A7B04f468d842c2eEa2fF43d71"
export OPENAI_API_BASE="https://api.aiguoguo199.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model vicuna-13b