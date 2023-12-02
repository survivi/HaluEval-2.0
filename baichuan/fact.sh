#!/bin/bash

ModelList=("baichuan2-7b-intermediate-00220" "baichuan2-7b-intermediate-00440" "baichuan2-7b-intermediate-00660" "baichuan2-7b-intermediate-00880" "baichuan2-7b-intermediate-01100" "baichuan2-7b-intermediate-01320" "baichuan2-7b-intermediate-01540" "baichuan2-7b-intermediate-01760" "baichuan2-7b-intermediate-01980" "baichuan2-7b-intermediate-02200" "baichuan2-7b-intermediate-02420")
for model in ${ModelList[*]}; do
    nohup python -u fact.py --all-files --model $model >> ./fact_log/fact_$model.log 2>&1 &
done