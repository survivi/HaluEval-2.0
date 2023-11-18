for file in Bio-Medical Finance Science Education Open-Domain
do
    nohup python -u judge.py --file $file --model chatgpt --data-dir "./fact/prompt_format/base/chatgpt/" --save-dir "./judge/prompt_format/base/chatgpt/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model chatgpt --data-dir "./fact/prompt_format/character_info/chatgpt/" --save-dir "./judge/prompt_format/character_info/chatgpt/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model chatgpt --data-dir "./fact/prompt_format/domain_info/chatgpt/" --save-dir "./judge/prompt_format/domain_info/chatgpt/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model chatgpt --data-dir "./fact/prompt_format/generate_demo/chatgpt/" --save-dir "./judge/prompt_format/generate_demo/chatgpt/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model chatgpt --data-dir "./fact/prompt_format/search_demo/chatgpt/" --save-dir "./judge/prompt_format/search_demo/chatgpt/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model chatgpt --data-dir "./fact/prompt_format/wrong_demo/chatgpt/" --save-dir "./judge/prompt_format/wrong_demo/chatgpt/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-7b-chat-hf --data-dir "./fact/prompt_format/base/llama2chat/" --save-dir "./judge/prompt_format/base/llama2chat/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-7b-chat-hf --data-dir "./fact/prompt_format/character_info/llama2chat/" --save-dir "./judge/prompt_format/character_info/llama2chat/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-7b-chat-hf --data-dir "./fact/prompt_format/domain_info/llama2chat/" --save-dir "./judge/prompt_format/domain_info/llama2chat/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-7b-chat-hf --data-dir "./fact/prompt_format/generate_demo/llama2chat/" --save-dir "./judge/prompt_format/generate_demo/llama2chat/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-7b-chat-hf --data-dir "./fact/prompt_format/search_demo/llama2chat/" --save-dir "./judge/prompt_format/search_demo/llama2chat/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-7b-chat-hf --data-dir "./fact/prompt_format/wrong_demo/llama2chat/" --save-dir "./judge/prompt_format/wrong_demo/llama2chat/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model chatgpt --data-dir "./fact/prompt_improvement/0-shot-cot/chatgpt/" --save-dir "./judge/prompt_improvement/0-shot-cot/chatgpt/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model chatgpt --data-dir "./fact/prompt_improvement/few-shot-cot/chatgpt/" --save-dir "./judge/prompt_improvement/few-shot-cot/chatgpt/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model chatgpt --data-dir "./fact/prompt_improvement/refine-q/chatgpt/" --save-dir "./judge/prompt_improvement/refine-q/chatgpt/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-7b-chat-hf --data-dir "./fact/prompt_improvement/0-shot-cot/llama2chat/" --save-dir "./judge/prompt_improvement/0-shot-cot/llama2chat/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-7b-chat-hf --data-dir "./fact/prompt_improvement/few-shot-cot/llama2chat/" --save-dir "./judge/prompt_improvement/few-shot-cot/llama2chat/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-7b-chat-hf --data-dir "./fact/prompt_improvement/refine-q/llama2chat/" --save-dir "./judge/prompt_improvement/refine-q/llama2chat/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-7b-chat-hf --data-dir "./fact/self_reflexion/7b/" --save-dir "./judge/self_reflexion/7b/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-13b-chat-hf --data-dir "./fact/self_reflexion/13b/" --save-dir "./judge/self_reflexion/13b/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-70b-chat-hf --data-dir "./fact/self_reflexion/70b/" --save-dir "./judge/self_reflexion/70b/" >> judge_$file.log 2>&1 &
    nohup python -u judge.py --file $file --model llama-2-70b-chat-hf --data-dir "./fact/self_reflexion/70b_raw/" --save-dir "./judge/self_reflexion/70b_raw/" >> judge_$file.log 2>&1 &
done