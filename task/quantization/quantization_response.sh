#!/bin/bash

# llama-2-7b-chat-hf 4bit
nohup python -u response.py --all-files --model llama-2-7b-chat-hf --load-in-4bit --data-dir "./annotation/query/" --save-dir "./quantization_response/llama-2-7b-chat-hf_INT4/" >> ./log/llama-2-7b-chat-hf_INT4.log 2>&1 &

# llama-2-13b-chat-hf 4bit
nohup python -u response.py --all-files --model llama-2-13b-chat-hf --load-in-4bit --data-dir "./annotation/query/" --save-dir "./quantization_response/llama-2-13b-chat-hf_INT4/" >> ./log/llama-2-13b-chat-hf_INT4.log 2>&1 &

# llama-2-7b-chat-hf 8bit
nohup python -u response.py --all-files --model llama-2-7b-chat-hf --load-in-8bit --data-dir "./annotation/query/" --save-dir "./quantization_response/llama-2-7b-chat-hf_INT8/" >> ./log/llama-2-7b-chat-hf_INT8.log 2>&1 &

# llama-2-13b-chat-hf 8bit
nohup python -u response.py --all-files --model llama-2-13b-chat-hf --load-in-8bit --data-dir "./annotation/query/" --save-dir "./quantization_response/llama-2-13b-chat-hf_INT8/" >> ./log/llama-2-13b-chat-hf_INT8.log 2>&1 &
