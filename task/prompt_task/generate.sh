for file in Bio-Medical Finance Science Education Open-Domain
do
    nohup python -u fact.py --file $file --model chatgpt --data-dir "./prompt_data/prompt_format/base/chatgpt/" --save-dir "./fact/prompt_format/base/chatgpt/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model chatgpt --data-dir "./prompt_data/prompt_format/character_info/chatgpt/" --save-dir "./fact/prompt_format/character_info/chatgpt/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model chatgpt --data-dir "./prompt_data/prompt_format/domain_info/chatgpt/" --save-dir "./fact/prompt_format/domain_info/chatgpt/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model chatgpt --data-dir "./prompt_data/prompt_format/generate_demo/chatgpt/" --save-dir "./fact/prompt_format/generate_demo/chatgpt/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model chatgpt --data-dir "./prompt_data/prompt_format/search_demo/chatgpt/" --save-dir "./fact/prompt_format/search_demo/chatgpt/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model chatgpt --data-dir "./prompt_data/prompt_format/wrong_demo/chatgpt/" --save-dir "./fact/prompt_format/wrong_demo/chatgpt/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-7b-chat-hf --data-dir "./prompt_data/prompt_format/base/llama2chat/" --save-dir "./fact/prompt_format/base/llama2chat/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-7b-chat-hf --data-dir "./prompt_data/prompt_format/character_info/llama2chat/" --save-dir "./fact/prompt_format/character_info/llama2chat/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-7b-chat-hf --data-dir "./prompt_data/prompt_format/domain_info/llama2chat/" --save-dir "./fact/prompt_format/domain_info/llama2chat/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-7b-chat-hf --data-dir "./prompt_data/prompt_format/generate_demo/llama2chat/" --save-dir "./fact/prompt_format/generate_demo/llama2chat/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-7b-chat-hf --data-dir "./prompt_data/prompt_format/search_demo/llama2chat/" --save-dir "./fact/prompt_format/search_demo/llama2chat/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-7b-chat-hf --data-dir "./prompt_data/prompt_format/wrong_demo/llama2chat/" --save-dir "./fact/prompt_format/wrong_demo/llama2chat/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model chatgpt --data-dir "./prompt_data/prompt_improvement/0-shot-cot/chatgpt/" --save-dir "./fact/prompt_improvement/0-shot-cot/chatgpt/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model chatgpt --data-dir "./prompt_data/prompt_improvement/few-shot-cot/chatgpt/" --save-dir "./fact/prompt_improvement/few-shot-cot/chatgpt/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model chatgpt --data-dir "./prompt_data/prompt_improvement/refine-q/chatgpt/" --save-dir "./fact/prompt_improvement/refine-q/chatgpt/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-7b-chat-hf --data-dir "./prompt_data/prompt_improvement/0-shot-cot/llama2chat/" --save-dir "./fact/prompt_improvement/0-shot-cot/llama2chat/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-7b-chat-hf --data-dir "./prompt_data/prompt_improvement/few-shot-cot/llama2chat/" --save-dir "./fact/prompt_improvement/few-shot-cot/llama2chat/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-7b-chat-hf --data-dir "./prompt_data/prompt_improvement/refine-q/llama2chat/" --save-dir "./fact/prompt_improvement/refine-q/llama2chat/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-7b-chat-hf --data-dir "./prompt_data/self_reflexion/7b/" --save-dir "./fact/self_reflexion/7b/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-13b-chat-hf --data-dir "./prompt_data/self_reflexion/13b/" --save-dir "./fact/self_reflexion/13b/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-70b-chat-hf --data-dir "./prompt_data/self_reflexion/70b/" --save-dir "./fact/self_reflexion/70b/" >> fact_$file.log 2>&1 &
    nohup python -u fact.py --file $file --model llama-2-70b-chat-hf --data-dir "./prompt_data/self_reflexion/70b_raw/" --save-dir "./fact/self_reflexion/70b_raw/" >> fact_$file.log 2>&1 &
done