echo "CURRENT MODEL: alpaca-7b"
for file in Bio-Medical Finance Science Education Open-Domain
do
    echo "(alpaca-7b) CURRENT FILE: $file"
    python rlhf_filter.py --model alpaca-7b --file $file
    # python rlhf_generate.py --model alpaca-7b --file $file
done
# echo "CURRENT MODEL: vicuna-7b"
# for file in Bio-Medical Finance Science Education Open-Domain
# do
#     echo "(vicuna-7b) CURRENT FILE: $file"
#     python rlhf_filter.py --model vicuna-7b --file $file
#     python rlhf_generate.py --model vicuna-7b --file $file
# done
# echo "CURRENT MODEL: vicuna-13b"
# for file in Bio-Medical Finance Science Education Open-Domain
# do
#     echo "(vicuna-13b) CURRENT FILE: $file"
#     python rlhf_filter.py --model vicuna-13b --file $file
#     python rlhf_generate.py --model vicuna-13b --file $file
# done