#!/bin/bash

export OPENAI_API_KEY="sk-"
export OPENAI_API_BASE="https://api.openai.com/v1"
echo "OPENAI_API_KEY is set to: $OPENAI_API_KEY"
echo "OPENAI_API_BASE is set to: $OPENAI_API_BASE"

ModelList=("chatgpt" "llama-2-7b-chat-hf")
for model in ${ModelList[*]}; do
    nohup python -u fact.py --file Wiki_Entity --model $model --data-dir ./wiki_entity_response/$model --save-dir ./fact/$model/ >> ./log/wiki_fact_$model.log 2>&1 &
done
