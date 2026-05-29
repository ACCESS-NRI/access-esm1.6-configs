### Changing MPI layout

To modify the MPI layout for the UM, there are 2 changes required:

1. Set the number of processes used in the longitude and latitude directions by setting the `UM_ATM_NPROCX` and `UM_ATM_NPROCY` variables in `atmosphere/um_env.yaml`. Then set the entry `UM_NPES` to be the product of `UM_ATM_NPROCX` and `UM_ATM_NPROCY`.
2. Set the number of CPUs requested by the atmosphere for the `payu` job by setting `ncpus` in the `atmosphere` section in `config.yaml` to the same value as `UM_NPES`.
