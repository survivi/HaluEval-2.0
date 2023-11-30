# #!/bin/bash
# export OPENAI_API_KEY="sk-CSw9knewT4AnOU9C21Fa655bEfA44e8591D7932e59632c7f"
# export OPENAI_API_BASE="https://api.aiguoguo199.com/v1"
# echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
# echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"
# # batch
# ModelList=("chatgpt" "text-davinci-002" "text-davinci-003" "llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "alpaca-7b" "vicuna-7b" "vicuna-13b")
# for model in ${ModelList[*]}; do
#     nohup python -u response.py --all-files --model $model >> $model.log 2>&1 &
# done
# # single model
# export CUDA_VISIBLE_DEVICES=0 && CUDA_VISIBLE_DEVICES=1 nohup python -u response.py --all-files --model chatgpt >> chatgpt.log 2>&1 &

export CUDA_VISIBLE_DEVICES=1 && CUDA_VISIBLE_DEVICES=2 nohup python -u response.py --all-files --model yulan-chat-2-13b-fp16 >> ./log/yulan.log 2>&1 &
