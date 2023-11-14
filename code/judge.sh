for file in Bio-Medical Finance Science Education Open-Domain
do
    nohup python -u judge.py --file $file --model claude-1 --data-dir "./fact/claude-1/" --save-dir "./judge/claude-1/" >> output.log 2>&1 &
    nohup python -u judge.py --file $file --model claude-2 --data-dir "./fact/claude-2/" --save-dir "./judge/claude-2/" >> output.log 2>&1 &
done