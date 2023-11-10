export CUDA_VISIBLE_DEVICES=1
python INT4.py --all-files --model llama-2-7b-chat-hf --data-dir ./query/ --save-dir ./response/llama-2-7b-chat-hf_INT4