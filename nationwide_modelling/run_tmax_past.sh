#!/bin/bash

#SBATCH -J mm_tmax_past_high      # job name
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=19
##SBATCH --mem-per-cpu=12000
#SBATCH --time=700:00:00 #batch job time limit
#SBATCH -p node
#SBATCH --mem 0  # use all memory available on cluster
#SBATCH --output past_tmax_high.%J.out   # output filename
#SBATCH --error  past_tmax_high.%J.err   # error filename
#SBATCH --mail-type=END,FAIL,TIME_LIMIT
#SBATCH --mail-user=johanna.malle@slf.ch
##SBATCH --exclusive

module unload python-3.7.6-gcc-9.1.0-2i2j24b
source activate /home/malle/miniconda3/envs/micromap

# export PYTHONUNBUFFERED=TRUE

export p=$SLURM_CPUS_PER_TASK # Size of multiprocessing pool
export N=19

srun python tmax_past.py $p $N > console_past_tmax.txt
