#!/bin/bash

nohup python -u judge.py --all-files --model llama-2-7b-chat-hf --data-dir "./fact/self_reflexion/7b/" --save-dir "./judge/self_reflexion/7b/" >> ./judge_log/self_reflexion_7b_judge.log 2>&1 &
nohup python -u judge.py --all-files --model llama-2-13b-chat-hf --data-dir "./fact/self_reflexion/13b/" --save-dir "./judge/self_reflexion/13b/" >> ./judge_log/self_reflexion_13b_judge.log 2>&1 &
nohup python -u judge.py --all-files --model llama-2-70b-chat-hf --data-dir "./fact/self_reflexion/70b/" --save-dir "./judge/self_reflexion/70b/" >> ./judge_log/self_reflexion_70b_judge.log 2>&1 &
nohup python -u judge.py --all-files --model llama-2-70b-chat-hf --data-dir "./fact/self_reflexion/70b_raw/" --save-dir "./judge/self_reflexion/70b_raw/" >> ./judge_log/self_reflexion_70b_raw_judge.log 2>&1 &
