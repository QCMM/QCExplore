#!/bin/bash

#SBATCH -J Tera_job
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --mem=24GB
#SBATCH --partition=long
#SBATCH --nodelist=i03
#SBATCH --gres=gpu:1


ID=$SLURM_JOB_ID
export SCRDIR=/scratch/${ID}
mkdir $SCRDIR

source /opt/anaconda/anaconda3/etc/profile.d/conda.sh && conda activate qcfractal
MODULEPATH=/opt/easybuild/modules/all
module load Terachem/1.9.4.lua

export OUTFILE=$SLURM_SUBMIT_DIR/out.dat

echo $SCRDIR
echo $SLURM_SUBMIT_DIR
echo $OUTFILE

bash $SLURM_SUBMIT_DIR/relax.sh $SCRDIR $OUTFILE 2>&1 

#cp -rp * $SLURM_SUBMIT_DIR/
#cd $SLURM_SUBMIT_DIR/
rm -rf $SCRDIR

