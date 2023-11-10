export CUDA_VISIBLE_DEVICES=0
python INT8.py --all-files --model llama-2-7b-chat-hf --data-dir ./query/ --save-dir ./response/llama-2-7b-chat-hf_INT8