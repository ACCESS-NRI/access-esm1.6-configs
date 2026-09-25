# Guidelines for running CMIP7 Assessment Fast Track simulations

This page provides guidelines for community members who will be running ACCESS-ESM1.6 experiments for the [CMIP7 Assessment Fast Track](https://wcrp-cmip.org/cmip-phases/cmip7/fast-track/). As part of the CMIP7 submission, there are requirements around provenance, documentation, and reproducibility, which will impact how the experiments will be run and shared.

This information on this page is fairly general, and ACCESS-NRI/CSIRO staff may provide you with further instructions specific to the experiment that you are running. 

If you haven't volunteered and would be interested in running Assessment Fast Track experiments, please take a look at [this table](https://forum.access-hive.org.au/t/fast-track/1625/7) for a list of the available experiments, and get in contact with Tilo Ziehn.


# Prerequisites

1. You will need an [NCI account](https://access-hive.org.au/getting_started/set_up_nci_account) and to [join project vk83](https://my.nci.org.au/mancini/project/vk83/join).
2. You will need to have completed the [UKMO licensing process](https://forum.access-hive.org.au/t/accessing-ukmo-licensed-models/6168).
3. You need to have a [GitHub account](https://github.com/) and authenticate it with [GitHub on gadi](https://forum.access-hive.org.au/t/setting-up-gh/4294)

---

# Background information
This section introduces some background concepts which will be helpful for understanding the instructions and guidelines further below. 

### Payu and running experiments
ACCESS-ESM1.6 is run using the program [Payu](https://payu.readthedocs.io/en/stable/). If you are unfamiliar with running models with Payu or need a refresher, please see [this guide on running ACCESS-ESM1.6](https://docs.access-hive.org.au/models/run_a_model/run_access-esm1p6/).

If you have any questions about running the model, ACCESS-NRI staff will be available to help via the ACCESS-Hive Forum.

### Configurations and experiments
#### Configurations
A Payu *model configuration* contains the complete collection of model settings, configuration files, and paths to input and restart files required to run a model. Payu configurations for ACCESS-ESM1.6 are kept as branches in the [access-esm1.6-configs](https://github.com/ACCESS-NRI/access-esm1.6-configs) GitHub repository, with `dev-` branches representing development versions of configurations and `release-` branches representing released configurations.

#### Experiments
Running a simulation involves cloning a configuration into a directory, called the control directory. When Payu runs a simulation, it keeps track of the configuration settings, input files, model executables, and restart files used for each run segment and records this information in a git commit in the Payu control directory. This information can be accessed later. For example, the configuration settings used for each segment of the ESM1.6 CMIP7 esm-piControl simulation are available to view [here](https://github.com/ACCESS-NRI/access-esm1.6-experiments/commits/esm-piControl-2026.04.14/). This sequence of commits are referred to as the Payu *runlogs*, and as a whole they form a Payu *experiment*.

On completion, ESM1.6 Payu experiments for the CMIP7 Assessment Fast Track will need to be uploaded to the [access-esm1.6-experiments](https://github.com/ACCESS-NRI/access-esm1.6-experiments) GitHub repository.

Payu *configurations* and *experiments* both contain all the information required to run a model, and either can be used to start a simulation.

--- 

# Instructions and guidelines
## Cloning and running an experiment
In most cases, ACCESS-NRI and CSIRO will provide you with a branch on the [access-esm1.6-experiments](https://github.com/ACCESS-NRI/access-esm1.6-experiments) GitHub repository which you can clone and run.

For example, to clone the (fictional) *example-experiment* [branch](https://github.com/ACCESS-Community-Hub/access-esm1.6-experiments/tree/example-experiment), you would first load the payu module, and use:
```
payu clone https://github.com/ACCESS-NRI/access-esm1.6-experiments -B example-experiment <control directory name>
```

!!! Warning
    CMIP7 requests a larger number of output variables than the default released configurations. Before running your experiment, please make sure that the settings have been adjusted to request the full set of CMIP7 outputs. To do this, navigate to the payu control directory and double check that:
        * The `atmosphere/STASHC` symlink points to `diagnostic_profiles/STASHC_CMIP7_core_<concentrations/emissions>`
        * The `ice/ice_history.nml` symlink points to `diagnostic_profiles/ice_history_CMIP7_high.nml`
        * The `ocean/diag_table` symlink points to `diagnostic_profiles/diag_table_CMIP7_core`
    See the [documentation section here](https://docs.access-hive.org.au/models/run_a_model/run_access-esm1p6/#controlling-the-diagnostics-output-by-the-model) for instructions on how to swap the diagnostic profiles.

Once the experiment has been cloned, you can `cd` into the control directory cloned in the command above and run it using the usual `payu run -n <nruns>` command.

!!! tip
    Some experiments will require a more complicated setup, such as scripts that need to be run before the initial simulation. Other experiments may need to be cloned from the [configuration repository](https://github.com/ACCESS-NRI/access-esm1.6-configs) rather than the [experiments repository](https://github.com/ACCESS-NRI/access-esm1.6-experiments). In these cases, ACCESS-NRI staff will provide you with specific instructions.



## Output syncing
Model outputs and restarts should be synced to a location on `/g/data` to prevent loss of data during the automatic cleanup of files on `/scratch`. We recommend configuring Payu to automatically sync the outputs and restarts to a location on `/g/data` by enabling the `sync` option in the `config.yaml`:

```yaml
# Sync options for automatically copying data from ephemeral scratch space to
# longer term storage
sync:
    enable: True # set path below and change to true
    restarts: True
    base_path: <Location on /g/data>
```

With the above changes, at the end of each run segment payu will automatically copy outputs and restarts to a directory matching your experiment's name under the location specified by `base_path`. For more information on automatic syncing, please see the [Payu documentation](https://payu.readthedocs.io/en/stable/config.html#:~:text=the%20PBS%20script.-,sync,-Sync%20archive%20to).

ACCESS-NRI and CSIRO staff can help determine the best location for syncing your data.


## Output archiving
Output and restart files for ESM1.6 fast track experiments are being archived to the `p73` project. Write access to `p73` is restricted and so CSIRO team members will be in contact with you to organise a data copy upon your simulations' completion.


## Pushing completed experiments back to the repository
Once your simulations are complete, the git runlogs will need to be pushed to the [access-esm1.6-experiments](https://github.com/ACCESS-NRI/access-esm1.6-experiments) GitHub repository.

If you are less familiar with Git and Github, ACCESS-NRI staff can complete this step. Let them know when your experiments are complete and they will instruct you on making the control directory and runlogs accessible to them.

If you are comfortable using git and GitHub, you are welcome to push the runlogs to the repository as follows:
1. First request write permissions on the [access-esm1.6-dev-experiments](https://github.com/ACCESS-Community-Hub/access-esm1.6-dev-experiments), by creating a [new-issue](https://github.com/ACCESS-NRI/access-esm1.6-experiments/issues) which lists the experiments you will be pushing to the repository.
2. Make sure to [authenticate your GitHub account on Gadi](https://forum.access-hive.org.au/t/setting-up-gh/4294)
3. Navigate to the payu control directory for the completed experiment, and run:
   ```
   $ git push origin HEAD
   ```

!!! warning
    If your experiment was originally cloned from the [configuration repository](https://github.com/ACCESS-NRI/access-esm1.6-configs) rather than the [experiments repository](https://github.com/ACCESS-NRI/access-esm1.6-experiments), the above instructions won't apply. ACCESS-NRI staff can provide you with specific instructions in this case, or can push the runlogs to the repository on their end.


## Crashes, perturbing atmospheric restarts, and reproducibiliy

During the simulations you may run into model crashes. These can occur due to many different reasons including transient errors on Gadi and numerical instabilities in the model. You're welcome to get in touch with ACCESS-NRI staff or add a [help request](https://forum.access-hive.org.au/t/access-help-and-support/908) to the ACCESS-Hive Forum for help with understanding the cause of a crash.

In general, we recommend the following approach for dealing with crashes:

First check the error logs for further information on the error, and try sweeping and rerunning using the payu commands from the experiment control directory:
```bash
$ payu sweep
$ payu run
```

If the same error occurs on the rerun, it may be due to a numerical instability in the atmosphere. This is typically accompanied by the following message in the `work/atmosphere/atm.fort6.pe0` atmosphere log file
```
  ==============================================
  initial Absolute Norm :    67248670.7694857     
  GCR(                     2 ) failed to converge in                     50 
  iterations. 
  Final Absolute Norm :    1049.99880463915     
  ==============================================
```
and perturbing the last atmosphere restart file may work as a workaround. It's important to do this in a reproducible way and to keep a record of any perturbations applied. Please follow the steps [outlined here](/inputs/restarts/#perturbing-an-atmospheric-restart-file), which will apply a reproducible perturbation and record it in the experiment runlogs.

!!! Tip
    The above error message indicates a failure in the atmosphere's numerical solver. This can be due to spurious numerical instabilities in the model (in which case perturbations can help), but can also occur due to other causes including problems in the configuration and input files which require more involved investigation.

Other types of crashes may require different workarounds. If you are unsure about what caused a crash or how to resolve it, we encourage you to add [help request](https://forum.access-hive.org.au/t/access-help-and-support/908) on the ACCESS-Hive forum, where ACCESS-NRI staff will be available to provide advice.

