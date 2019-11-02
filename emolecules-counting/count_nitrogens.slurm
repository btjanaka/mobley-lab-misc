#!/bin/bash
# USAGE:
#   sbatch count_nitrogens.slurm

#SBATCH --job-name="count-nitrogens"
#SBATCH --partition=ilg2.3
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4gb
#SBATCH --time=30:00:00
#SBATCH --distribution=block:cyclic
#--------------

# Informational output
echo "=================================== SLURM JOB ==================================="
echo
echo "The job will be started on the following node(s):"
echo $SLURM_JOB_NODELIST
echo
echo "Slurm User:         $SLURM_JOB_USER"
echo "Run Directory:      $(pwd)"
echo "Job ID:             $SLURM_JOB_ID"
echo "Job Name:           $SLURM_JOB_NAME"
echo "Partition:          $SLURM_JOB_PARTITION"
echo "Number of nodes:    $SLURM_JOB_NUM_NODES"
echo "Number of tasks:    $SLURM_NTASKS"
echo "Submitted From:     $SLURM_SUBMIT_HOST"
echo "Submit directory:   $SLURM_SUBMIT_DIR"
echo "=================================== SLURM JOB ==================================="
echo


cd $SLURM_SUBMIT_DIR
echo 'Working Directory:'
pwd

date

EMOL="/data15/mobley_temp/kyud/Forcefield_Project/eMolecule/minimized_files/"
count_nitrogens \
  --dirs ${EMOL}/eMolecules_1/SMIRNOFF,${EMOL}/eMolecules_2/SMIRNOFF,${EMOL}/eMolecules_3/SMIRNOFF,${EMOL}/eMolecules_4/SMIRNOFF,${EMOL}/eMolecules_5/SMIRNOFF,${EMOL}/eMolecules_6/SMIRNOFF,${EMOL}/eMolecules_7/SMIRNOFF,${EMOL}/eMolecules_8/SMIRNOFF,${EMOL}/eMolecules_9/SMIRNOFF \
  --output ./results.md

date
