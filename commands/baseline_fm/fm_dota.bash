#!/bin/bash

#SBATCH --job-name=fm
#SBATCH --error=slurm/fm_err
#SBATCH --out=slurm/fm_out
#SBATCH --exclusive
#SBATCH --partition=ser-par-10g-5
#SBATCH -N 1
#SBATCH -D /home/chen.zhe/GAE/model

source activate myenv
work=/home/chen.zhe/GAE/model
cd $work

python3.6 baseline_fm_tf.py --dataset=dota --fm_order=3 --fm_rank=200 --fm_epoch=10 --fm_reg=100. --fm_featconfig=one_way_two_teams

