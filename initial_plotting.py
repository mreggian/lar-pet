# Author: Marina Reggiani-Guzzo
# Last modified: April 1, 2026
# Description: create a Pandas Dataframe from a HDF5 file.

import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_dataframe(filename, group):

    # open HDF5 file
    with h5py.File(filename, 'r') as f:
        #print(f"Keys: {f.keys()}")
        dataset = f[group]
        data = dataset[()] # [:10] for a subset

    columns = {}

    print("List of variables:")
    for name in data.dtype.names:
        field = data[name]

        # If it's a scalar column
        if field.ndim == 1:
            columns[name] = field

        # If it's a vector (e.g. shape (N, 3))
        else:
            for i in range(field.shape[1]):
                columns[f"{name}_{i}"] = field[:, i]

    df = pd.DataFrame(columns)

    return df

def print_df_summary(df, group):

    print("\nSummary")
    print(f"> Group: {group}")
    print(f"> Number of entries: {len(df)}")
    print(f"> Number of interactions: {df['event_id'].nunique()}")
    print(f"> Columns: {df.columns}")
  
# Create a dataframe per group in HDF5 file
df_mc_hdr = create_dataframe('/Users/mreggian/Downloads/604.EDEPSIM.hdf5', 'mc_hdr')
df_mc_stack = create_dataframe('/Users/mreggian/Downloads/604.EDEPSIM.hdf5', 'mc_stack')
df_segments = create_dataframe('/Users/mreggian/Downloads/604.EDEPSIM.hdf5', 'segments')
df_trajectories = create_dataframe('/Users/mreggian/Downloads/604.EDEPSIM.hdf5', 'trajectories')
df_vertices = create_dataframe('/Users/mreggian/Downloads/604.EDEPSIM.hdf5', 'vertices')

# Print a summary regarding each dataframe (add more information to this summary as you wish)
names = ["mc_hdr", "mc_stack", "segments", "trajectories", "vertices"]
for i, df in enumerate([df_mc_hdr, df_mc_stack, df_segments, df_trajectories, df_vertices]):
    print_df_summary(df.copy(), names[i])

print(df_trajectories[['event_id','traj_id','parent_id','pdg_id','start_process','start_subprocess','E_start','E_end']].head(30))

# ======================================================================================

# Plot PDG code for primary particle (parent_id==-1) and secondary particles produced via Compton scattering (parent_id==0 & start_process==2 & start_subprocess==13)

plt.hist(df_trajectories.loc[df_trajectories.parent_id == -1, "pdg_id"], label="Primary")
plt.hist(df_trajectories.loc[(df_trajectories.parent_id==0) & (df_trajectories.start_process==2) & (df_trajectories.start_subprocess==13), "pdg_id"], label="Secondary Particle via Compton Scattering")
plt.legend()
plt.ylabel("count")
plt.xlabel("PDG code")
plt.show()

# ======================================================================================

# Plot number of Compton scatterings per event.

multiplicity_array = []

# Loop over events
for event_id in df_trajectories["event_id"].drop_duplicates().tolist():

    # Count how many electrons (pdg_id==11) produced via compton scattering (start_process==2 & start_subprocess==13) from primary photon (parent_id==0)
    query_compton_multiplicity = f"event_id=={event_id} & pdg_id==11 & parent_id==0 & start_process==2 & start_subprocess==13"
    df_temp = df_trajectories.query(query_compton_multiplicity)
    multiplicity_array.append(len(df_temp))

bins = range(min(multiplicity_array), max(multiplicity_array) + 2)
plt.hist(multiplicity_array, bins=bins, edgecolor='black')
plt.title(f"Total number of events = {df_trajectories['event_id'].nunique()}")
plt.xlabel("Number of Compton Scatterings per Event")
plt.ylabel("Number of Events")
plt.show()

# ======================================================================================