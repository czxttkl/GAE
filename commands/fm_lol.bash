#!/bin/bash

#SBATCH --job-name=fm
#SBATCH --error=slurm/fm
#SBATCH --out=slurm/fm
#SBATCH --exclusive
#SBATCH --partition=ser-par-10g-5
#SBATCH -N 1
#SBATCH -D /home/chen.zhe/GAE/model

source activate myenv
work=/home/chen.zhe/GAE/model
cd $work

python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=0.00001 --fm_featconfig=champion_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=0.0001 --fm_featconfig=champion_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=0.001 --fm_featconfig=champion_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=0.01 --fm_featconfig=champion_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=0.1 --fm_featconfig=champion_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=1.0 --fm_featconfig=champion_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=10 --fm_featconfig=champion_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=100 --fm_featconfig=champion_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=1000 --fm_featconfig=champion_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=10000 --fm_featconfig=champion_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=0.00001 --fm_featconfig=summoner_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=0.0001 --fm_featconfig=summoner_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=0.001 --fm_featconfig=summoner_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=0.01 --fm_featconfig=summoner_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=0.1 --fm_featconfig=summoner_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=1.0 --fm_featconfig=summoner_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=10 --fm_featconfig=summoner_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=100 --fm_featconfig=summoner_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=1000 --fm_featconfig=summoner_one_team
python3.6 baseline_fm_tf.py --fm_order=1 --fm_rank=2 --fm_epoch=10 --fm_reg=10000 --fm_featconfig=summoner_one_team

