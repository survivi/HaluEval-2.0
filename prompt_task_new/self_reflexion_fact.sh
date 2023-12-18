#!/bin/bash

nohup python -u fact.py --all-files --model llama-2-7b-chat-hf --data-dir "./prompt_response/self_reflexion/7b/" --save-dir "./fact/self_reflexion/7b/" >> ./fact_log/self_reflexion_7b_fact.log 2>&1 &
nohup python -u fact.py --all-files --model llama-2-13b-chat-hf --data-dir "./prompt_response/self_reflexion/13b/" --save-dir "./fact/self_reflexion/13b/" >> ./fact_log/self_reflexion_13b_fact.log 2>&1 &
nohup python -u fact.py --all-files --model llama-2-70b-chat-hf --data-dir "./prompt_response/self_reflexion/70b/" --save-dir "./fact/self_reflexion/70b/" >> ./fact_log/self_reflexion_70b_fact.log 2>&1 &
