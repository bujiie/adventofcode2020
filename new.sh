#!/usr/bin/env bash

day=$1

challenge_dir="day${1}"
input_dir="input"
sample_input_file="sample.in"
problem_input_file="problem.in"

mkdir $challenge_dir
cp __template.py "${challenge_dir}/pt1.py"
cd $challenge_dir
chmod 755 pt1.py

mkdir $input_dir
cd $input_dir
touch $sample_input_file $problem_input_file





