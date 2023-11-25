# python metric.py --model llama-2-7b-chat-hf --data-dir ./judge/llama-2-7b-chat-hf_beam_judge/
# python metric.py --model llama-2-7b-chat-hf --data-dir ./judge/llama-2-7b-chat-hf_top-k_judge/
# python metric.py --model llama-2-7b-chat-hf --data-dir ./judge/llama-2-7b-chat-hf_top-p_judge/
# python metric.py --model llama-2-7b-chat-hf --data-dir ./judge/llama-2-7b-chat-hf_top-p_2_judge/
# python metric.py --model llama-2-7b-chat-hf --data-dir ./judge/llama-2-7b-chat-hf_top-p_4_judge/
# python metric.py --model llama-2-7b-chat-hf --data-dir ./judge/llama-2-7b-chat-hf_top-p_6_judge/
# python metric.py --model llama-2-7b-chat-hf --data-dir ./judge/llama-2-7b-chat-hf_top-p_8_judge/
# python metric.py --model llama-2-7b-chat-hf --data-dir ./judge/llama-2-7b-chat-hf_top-p_10_judge/

# python metric.py --model llama-7b --data-dir ./judge/complexity/
# python metric.py --model llama-7b --data-dir ./judge/scaling/
# python metric.py --model llama-7b --data-dir ./judge/diversity/
# python metric.py --model llama-7b --data-dir ./judge/difficulty/

ModelList=("chatgpt" "text-davinci-002" "text-davinci-003" "llama-2-7b-chat-hf" "llama-2-13b-chat-hf" "alpaca-7b" "vicuna-7b" "vicuna-13b")
for model in ${ModelList[*]}; do
    python metric.py --model $model --data-dir "./task/main/judge/$model"
done