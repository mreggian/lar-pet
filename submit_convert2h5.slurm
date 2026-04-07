# Author: Lauren Sdun
# Last modified: April 7, 2026
# Description: # submit a batch job that runs the ROOT to HDF5 conversion inside the ARCUBE Shifter container for a single ROOT file. The input and output files can be changed in lines 34-35.

#!/bin/bash

#SBATCH --account=dune
#SBATCH --constraint=cpu
#SBATCH --qos=shared
#SBATCH --nodes=1
#SBATCH --time=00:10:00
#SBATCH --job-name=convert_h5
#SBATCH --output=logs/convert_%j.out
#SBATCH --error=logs/convert_%j.err

# Ensure the log directory exists
mkdir -p logs

export ARCUBE_CONTAINER=mjkramer/sim2x2:ndlar011

shifter --image=$ARCUBE_CONTAINER --module=none -- bash -lc '
source /environment
cd /global/cfs/cdirs/dune/users/lasdun/2x2_sim/run-convert2h5

python3 -m pip install --user fire h5py tqdm

# After going from ROOT 6.14.06 to 6.28.06, apparently we need to point CPATH to
# the edepsim-io headers. Otherwise convert2h5 fails. (This "should" be set in
# the container already.)
export CPATH=$EDEPSIM/include/EDepSim:$CPATH

# Execute the job script.
python3 ./convert_edepsim_roottoh5.py \
  --input_file /global/cfs/cdirs/dune/users/lasdun/2x2_sim/run-edep-sim/Na22/job_array_output_10events/1.EDEPSIM.root \
  --output_file /global/cfs/cdirs/dune/users/lasdun/2x2_sim/run-edep-sim/Na22/job_array_output_10events/1.EDEPSIM.hdf5
'
