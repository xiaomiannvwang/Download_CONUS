#!/bin/bash

#SBATCH --ntasks=1
#SBATCH --time=3:00:00
#SBATCH --export==devel/python/3.6_intel
#SBATCH --job-name= Conus2.5 Download

export KMP_AFFINITY=compact
module load ${MODULE}


export PATH=$PATH:/pfs/work6/workspace/scratch/ov0392-KeShi_Prak-0/cuda90/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/pfs/work6/workspace/scratch/ov0392-KeShi_Prak-0/cuda90/cuda90/lib64

cd /pfs/work6/workspace/scratch/ov0392-CONUS2.5-0
source env6/bin/activate



cd /pfs/work6/workspace/scratch/ov0392-CONUS2.5-0/github

python download_CONUS_2.5_multiprocessing_v1_check_dir_umfolder_v2_scc_logging.py
