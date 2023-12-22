#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

ModelList=("chatgpt" "llama-2-7b-chat-hf")
for model in ${ModelList[*]}; do
    nohup python -u judge.py --file Wiki_Entity --model $model --data-dir ./fact/$model --save-dir ./wiki_entity_judge/$model/ >> ./log/wiki_judge_$model.log 2>&1 &
done
