# !/bin/bash

## Calculate Metrics for Each Task

# advanced_decoding
DirList=("gns_response" "fns_response")
for dir in ${DirList[*]}; do
    python metric.py --model llama-2-7b-chat-hf --data-dir "./task/advanced_decoding/advanced_decoding_judge/$dir"
done


# decoding_strategy
DirList=("chatgpt_greedy" "chatgpt_top-p" "llama-2-7b-chat-hf_beam" "llama-2-7b-chat-hf_top-k" "llama-2-7b-chat-hf_top-p" "llama-2-7b-chat-hf_greedy")
for dir in ${DirList[*]}; do
    model=${dir%%_*}
    python metric.py --model $model --data-dir "./task/decoding-strategy/decoding-strategy_judge/$dir"
done
DirList=("llama-2-7b-chat-hf_top-p_2" "llama-2-7b-chat-hf_top-p_4" "llama-2-7b-chat-hf_top-p_6" "llama-2-7b-chat-hf_top-p_8" "llama-2-7b-chat-hf_top-p_10")
for dir in ${DirList[*]}; do
    model=${dir%%_*}
    python metric.py --model $model --data-dir "./task/decoding-strategy/decoding-strategy_judge/$dir"
done
DirList=("chatgpt_top-p_2" "chatgpt_top-p_4" "chatgpt_top-p_6" "chatgpt_top-p_8" "chatgpt_top-p_10")
for dir in ${DirList[*]}; do
    model=${dir%%_*}
    python metric.py --model $model --data-dir "./task/decoding-strategy/decoding-strategy_judge/$dir"
done
DirList=("llama-2-13b-chat-hf_greedy" "llama-2-70b-chat-hf_greedy" "vicuna-7b_greedy" "vicuna-13b_greedy" "alpaca-7b_greedy")
for dir in ${DirList[*]}; do
    model=${dir%%_*}
    python metric.py --model $model --data-dir "./task/decoding-strategy/decoding-strategy_judge/$dir"
done


# ir
DirList=("response_1docs_top1" "response_5docs_top5" "response_10docs_top10" "response_1docs_top2" "response_1docs_top5" "response_1docs_top10")
ModelList=("chatgpt" "llama-2-7b-chat-hf")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        python metric.py --model $model --data-dir "./task/ir/ir_judge/$dir/$model"
    done
done
DirList=("response_2docs_top2")
ModelList=("chatgpt" "llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "vicuna-7b" "vicuna-13b")
for model in ${ModelList[*]}; do
    for dir in ${DirList[*]}; do
        python metric.py --model $model --data-dir "./task/ir/ir_judge/$dir/$model"
    done
done


# main
ModelList=("chatgpt" "text-davinci-002" "text-davinci-003" "llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "alpaca-7b" "vicuna-7b" "vicuna-13b" "claude-1" "claude-2" "yulan-chat-2-13b-fp16")
for model in ${ModelList[*]}; do
    python metric.py --model $model --data-dir "./task/main/judge/$model"
done


# pretrain
ModelList=("baichuan2-7b-intermediate-00220" "baichuan2-7b-intermediate-00440" "baichuan2-7b-intermediate-00660" "baichuan2-7b-intermediate-00880" "baichuan2-7b-intermediate-01100" "baichuan2-7b-intermediate-01320" "baichuan2-7b-intermediate-01540" "baichuan2-7b-intermediate-01760" "baichuan2-7b-intermediate-01980" "baichuan2-7b-intermediate-02200" "baichuan2-7b-intermediate-02420")
for model in ${ModelList[*]}; do
    python metric.py --model $model --data-dir "./task/pretrain/baichuan_judge/$model"
done
ModelList=("falcon-40b" "galactica-30b" "gpt-neox-20b")
for model in ${ModelList[*]}; do
    python metric.py --model $model --data-dir "./task/pretrain/pretrain_judge/$model"
done


# prompt_task
DirList=("0-shot" "base" "character_info" "domain_info" "few-shot" "in-context_demo" "mannual_desc" "refine_q" "retrieved_demo" "reverse_pos" "synthetic_demo" "synthetic_desc" "wrong_demo")
for dir in ${DirList[*]}; do
    python metric.py --model chatgpt --data-dir "./task/prompt_task/prompt_judge/chatgpt/$dir"
done
DirList=("0-shot" "base" "character_info" "domain_info" "few-shot" "in-context_demo" "mannual_desc" "refine_q" "retrieved_demo" "reverse_pos" "synthetic_demo" "synthetic_desc" "wrong_demo")
for dir in ${DirList[*]}; do
    python metric.py --model llama-2-7b-chat-hf --data-dir "./task/prompt_task/prompt_judge/llama-2-7b-chat-hf/$dir"
done
ModelList=("llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "llama-2-70b-chat-hf")
for model in ${ModelList[*]}; do
    python metric.py --model $model --data-dir "./task/prompt_task/prompt_judge/self_reflexion/$model"
done


# quantization
DirList=("llama-2-7b-chat-hf_INT4" "llama-2-7b-chat-hf_INT8" "llama-2-13b-chat-hf_INT4" "llama-2-13b-chat-hf_INT8")
for dir in ${DirList[*]}; do
    model=${dir%%_*}
    python metric.py --model $model --data-dir "./task/quantization/quantization_judge/$dir"
done


# RLHF
ModelList=("alpaca-7b" "vicuna-7b")
for model in ${ModelList[*]}; do
    python metric.py --model $model --data-dir "./task/RLHF/rlhf_judge/$model"
done


# SFT
DirList=("complexity" "difficulty" "diversity" "scaling")
for dir in ${DirList[*]}; do
    python metric.py --model llama-7b --data-dir "./task/SFT/sft_judge/$dir"
done
DirList=("flan" "sharegpt" "sinstruct" "sinstruct_sharegpt" "sinstruct_sharegpt_flan_10k")
for dir in ${DirList[*]}; do
    python metric.py --model llama-7b --data-dir "./task/SFT/sft_judge/$dir"
done
python metric.py --model llama-7b --data-dir "./task/SFT/sft_judge/llama-7b/"


# wiki_entity
ModelList=("chatgpt" "llama-2-7b-chat-hf")
for model in ${ModelList[*]}; do
    python metric.py --model $model --data-dir "./task/wiki_entity/wiki_entity_judge/$model"
done
