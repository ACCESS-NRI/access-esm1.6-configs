# ACCESS-ESM1.6 configurations and experiments

ACCESS-NRI supports and maintains several released configurations for ACCESS-ESM1.6, which have primarily been used to run CMIP7 experiments. These configurations will be actively updated with bug fixes and improvements. Documentation on how these configurations have been set up is available under the [configurations](configs_experiments/configurations) drop down.

Many other CMIP7 experiments have been run using ACCESS-ESM1.6 which do not have ACCESS-NRI released or supported configurations. These experiments will not automatically include improvements and updates, and manual updates may be required to rerun them. Documentation on how these experiments were set up is available under the [experiments](configs_experiments/experiments) drop down.

# Common settings

There are some aspects which are consistent across all configurations and experiments.

* **Changing the MPI layout**: When changing the MPI layout, modifications are required in both the `config.yaml` and the respective component's configuration. See the [Changing number of processes](https://docs.access-hive.org.au/models/build_a_model/build_source_code/#changing-number-of-processes-for-linaro-ddt) section under *Build a Model* in the Hive docs for information on setting this for each model component.
