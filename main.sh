#!/bin/bash
# alpaca-7b
export CUDA_VISIBLE_DEVICES=8
python main.py --all-files --model alpaca-7b --data-dir ./add/alpaca-7b/ --save-dir ./add_response/alpaca-7b/
# llama-2-7b-chat-hf
export CUDA_VISIBLE_DEVICES=8
python main.py --all-files --model llama-2-7b-chat-hf --data-dir ./add/llama-2-7b-chat-hf/ --save-dir ./add_response/llama-2-7b-chat-hf/
# llama-2-7b-chat-hf_beam
export CUDA_VISIBLE_DEVICES=8
python main.py --all-files --model llama-2-7b-chat-hf --data-dir ./add/llama-2-7b-chat-hf_beam/ --save-dir ./add_response/llama-2-7b-chat-hf_beam/ --num-beams 5 --early-stopping
# llama-2-7b-chat-hf_INT4
export CUDA_VISIBLE_DEVICES=8
python INT4.py --all-files --model llama-2-7b-chat-hf --data-dir ./add/llama-2-7b-chat-hf_INT4/ --save-dir ./add_response/llama-2-7b-chat-hf_INT4/
# llama-2-7b-chat-hf_INT8
export CUDA_VISIBLE_DEVICES=7
python INT8.py --all-files --model llama-2-7b-chat-hf --data-dir ./add/llama-2-7b-chat-hf_INT8/ --save-dir ./add_response/llama-2-7b-chat-hf_INT8/
# llama-2-7b-chat-hf_top-k
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-2-7b-chat-hf --data-dir ./add/llama-2-7b-chat-hf_top-k/ --save-dir ./add_response/llama-2-7b-chat-hf_top-k/ --do-sample --top-k 50
# llama-2-7b-chat-hf_top-p
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-2-7b-chat-hf --data-dir ./add/llama-2-7b-chat-hf_top-p/ --save-dir ./add_response/llama-2-7b-chat-hf_top-p/ --do-sample --top-k 0 --top-p 0.5
# llama-2-7b-chat-hf_top-p_2
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-2-7b-chat-hf --data-dir ./add/llama-2-7b-chat-hf_top-p_2/ --save-dir ./add_response/llama-2-7b-chat-hf_top-p_2/ --do-sample --top-k 0 --top-p 0.2
# llama-2-7b-chat-hf_top-p_4
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-2-7b-chat-hf --data-dir ./add/llama-2-7b-chat-hf_top-p_4/ --save-dir ./add_response/llama-2-7b-chat-hf_top-p_4/ --do-sample --top-k 0 --top-p 0.4
# llama-2-7b-chat-hf_top-p_6
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-2-7b-chat-hf --data-dir ./add/llama-2-7b-chat-hf_top-p_6/ --save-dir ./add_response/llama-2-7b-chat-hf_top-p_6/ --do-sample --top-k 0 --top-p 0.6
# llama-2-7b-chat-hf_top-p_8
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-2-7b-chat-hf --data-dir ./add/llama-2-7b-chat-hf_top-p_8/ --save-dir ./add_response/llama-2-7b-chat-hf_top-p_8/ --do-sample --top-k 0 --top-p 0.8
# llama-2-7b-chat-hf_top-p_10
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-2-7b-chat-hf --data-dir ./add/llama-2-7b-chat-hf_top-p_10/ --save-dir ./add_response/llama-2-7b-chat-hf_top-p_10/ --do-sample --top-k 0 --top-p 1.0
# llama-2-13b-chat-hf
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-2-13b-chat-hf --data-dir ./add/llama-2-13b-chat-hf/ --save-dir ./add_response/llama-2-13b-chat-hf/
# llama-2-13b-chat-hf_INT4
export CUDA_VISIBLE_DEVICES=9
python INT4.py --all-files --model llama-2-13b-chat-hf --data-dir ./add/llama-2-13b-chat-hf_INT4/ --save-dir ./add_response/llama-2-13b-chat-hf_INT4/
# llama-2-13b-chat-hf_INT8
export CUDA_VISIBLE_DEVICES=9
python INT8.py --all-files --model llama-2-13b-chat-hf --data-dir ./add/llama-2-13b-chat-hf_INT8/ --save-dir ./add_response/llama-2-13b-chat-hf_INT8/
# llama-7b
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model llama-7b --data-dir ./add/llama-7b/ --save-dir ./add_response/llama-7b/
# text-davinci-002
export OPENAI_API_KEY="sk-AZFhjE7fZW33inqK0701D5A7B04f468d842c2eEa2fF43d71"
export OPENAI_API_BASE="https://api.aiguoguo199.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"
python main.py --all-files --model text-davinci-002 --data-dir ./add/text-davinci-002/ --save-dir ./add_response/text-davinci-002/
# text-davinci-003
export OPENAI_API_KEY="sk-AZFhjE7fZW33inqK0701D5A7B04f468d842c2eEa2fF43d71"
export OPENAI_API_BASE="https://api.aiguoguo199.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"
python main.py --all-files --model text-davinci-003 --data-dir ./add/text-davinci-003/ --save-dir ./add_response/text-davinci-003/
# vicuna-7b
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model vicuna-7b --data-dir ./add/vicuna-7b/ --save-dir ./add_response/vicuna-7b/
# vicuna-13b
export CUDA_VISIBLE_DEVICES=9
python main.py --all-files --model vicuna-13b --data-dir ./add/vicuna-13b/ --save-dir ./add_response/vicuna-13b/
# chatgpt
export OPENAI_API_KEY="sk-AZFhjE7fZW33inqK0701D5A7B04f468d842c2eEa2fF43d71"
export OPENAI_API_BASE="https://api.aiguoguo199.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"
python main.py --all-files --model chatgpt --data-dir ./add/chatgpt/ --save-dir ./add_response/chatgpt/