import optparse

parser = optparse.OptionParser(usage="usage: player0_vs_player1")
(kwargs, args) = parser.parse_args()

command_str = []

for arg in args:
    p0_str, p1_str = arg.split('_vs_')
    job_name = arg
    s = \
"""#!/bin/bash

#SBATCH --job-name={}
#SBATCH --error=slurm/{}_err
#SBATCH --out=slurm/{}_out
#SBATCH --exclusive
#SBATCH --partition=ser-par-10g-5
#SBATCH -N 1
#SBATCH -D /home/chen.zhe/GAE/recom_sys_captain_mode

source activate myenv
work=/home/chen.zhe/GAE/recom_sys_captain_mode
cd $work

python3.6 -u experiment.py --env_path=NN_hiddenunit120_dota.pickle --num_matches=500 --p0={} --p1={} > slurm/{}_out
""".format(job_name, job_name, job_name, p0_str, p1_str, job_name)
    with open(job_name + '.bash', 'w') as f:
        f.write(s)
    command_str.append('sbatch ' + job_name + '.bash')

print(' && '.join(command_str))