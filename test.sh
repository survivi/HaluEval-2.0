export CUDA_VISIBLE_DEVICES="8,9"
python test.py --all-files --model llama-2-13b-hf --data-dir "./data/" --save-dir "./temp/"