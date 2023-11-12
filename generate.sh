python generate.py --all-files --model alpaca-7b --data-dir "./add_response/alpaca-7b/" --save-dir "./add_fact/alpaca-7b/"
python generate.py --all-files --model llama-2-7b-chat-hf --data-dir "./add_response/llama-2-7b-chat-hf/" --save-dir "./add_fact/llama-2-7b-chat-hf/"
python generate.py --all-files --model llama-2-7b-chat-hf --data-dir "./add_response/llama-2-7b-chat-hf_beam/" --save-dir "./add_fact/llama-2-7b-chat-hf_beam/"
python generate.py --all-files --model llama-2-7b-chat-hf --data-dir "./add_response/llama-2-7b-chat-hf_top-k/" --save-dir "./add_fact/llama-2-7b-chat-hf_top-k/"
python generate.py --all-files --model llama-2-7b-chat-hf --data-dir "./add_response/llama-2-7b-chat-hf_top-p/" --save-dir "./add_fact/llama-2-7b-chat-hf_top-p/"
python generate.py --all-files --model llama-2-7b-chat-hf --data-dir "./add_response/llama-2-7b-chat-hf_top-p_2/" --save-dir "./add_fact/llama-2-7b-chat-hf_top-p_2/"
python generate.py --all-files --model llama-2-7b-chat-hf --data-dir "./add_response/llama-2-7b-chat-hf_top-p_4/" --save-dir "./add_fact/llama-2-7b-chat-hf_top-p_4/"
python generate.py --all-files --model llama-2-7b-chat-hf --data-dir "./add_response/llama-2-7b-chat-hf_top-p_6/" --save-dir "./add_fact/llama-2-7b-chat-hf_top-p_6/"
python generate.py --all-files --model llama-2-7b-chat-hf --data-dir "./add_response/llama-2-7b-chat-hf_top-p_8/" --save-dir "./add_fact/llama-2-7b-chat-hf_top-p_8/"
python generate.py --all-files --model llama-2-7b-chat-hf --data-dir "./add_response/llama-2-7b-chat-hf_top-p_10/" --save-dir "./add_fact/llama-2-7b-chat-hf_top-p_10/"
python generate.py --all-files --model llama-2-13b-chat-hf --data-dir "./add_response/llama-2-13b-chat-hf/" --save-dir "./add_fact/llama-2-13b-chat-hf/"
python generate.py --all-files --model text-davinci-002 --data-dir "./add_response/text-davinci-002/" --save-dir "./add_fact/text-davinci-002/"
python generate.py --all-files --model text-davinci-003 --data-dir "./add_response/text-davinci-003/" --save-dir "./add_fact/text-davinci-003/"
python generate.py --all-files --model vicuna-7b --data-dir "./add_response/vicuna-7b/" --save-dir "./add_fact/vicuna-7b/"
python generate.py --all-files --model vicuna-13b --data-dir "./add_response/vicuna-13b/" --save-dir "./add_fact/vicuna-13b/"
python generate.py --all-files --model claude-1 --data-dir "./response/claude-1/" --save-dir "./fact/claude-1/"
python generate.py --all-files --model claude-2 --data-dir "./response/claude-2/" --save-dir "./fact/claude-2/"
python generate.py --all-files --model llama-2-7b-chat-hf --data-dir "./response/llama-2-7b-chat-hf_INT4/" --save-dir "./fact/llama-2-7b-chat-hf_INT4/"
python generate.py --all-files --model llama-2-7b-chat-hf --data-dir "./response/llama-2-7b-chat-hf_INT8/" --save-dir "./fact/llama-2-7b-chat-hf_INT8/"
python generate.py --all-files --model llama-2-13b-chat-hf --data-dir "./response/llama-2-13b-chat-hf_INT4/" --save-dir "./fact/llama-2-13b-chat-hf_INT4/"
python generate.py --all-files --model llama-2-13b-chat-hf --data-dir "./response/llama-2-13b-chat-hf_INT8/" --save-dir "./fact/llama-2-13b-chat-hf_INT8/"
python generate.py --all-files --model llama-7b --data-dir "./response/llama-7b/" --save-dir "./fact/llama-7b/"