# Guidelines for running CMIP7 Assessment Fast Track simulations

This page provides guidelines for community members who will be running ACCESS-ESM1.6 experiments for the [CMIP7 Assessment Fast Track](https://wcrp-cmip.org/cmip-phases/cmip7/fast-track/). As part of the CMIP7 submission, there are requirements around provenance, documentation, and reproducibility, which will impact how your experiments should be run and shared.

This information on this page is fairly general, and ACCESS-NRI/CSIRO staff may provide you with further instructions specific to the experiment that you are running. 

If you haven't volunteered and would be interested in running Assessment Fast Track experiments, please take a look at [this table](https://forum.access-hive.org.au/t/fast-track/1625/7) for a list of the available experiments, and get in contact with Tilo Ziehn.


# Prerequisites

1. You will need an [NCI account](https://access-hive.org.au/getting_started/set_up_nci_account) and to [join project vk83](https://my.nci.org.au/mancini/project/vk83/join).
2. You will need to have completed the [UKMO licensing process](https://forum.access-hive.org.au/t/accessing-ukmo-licensed-models/6168).
3. You need to have a [GitHub account](https://github.com/) and authenticate it with [GitHub on gadi](https://forum.access-hive.org.au/t/setting-up-gh/4294)
4. You will need write permissions on the [access-esm1.6-dev-experiments](https://github.com/ACCESS-Community-Hub/access-esm1.6-dev-experiments) GitHub repository. To request access, create a [new issue](https://github.com/ACCESS-Community-Hub/access-esm1.6-dev-experiments/issues) using the *Repository access request* template.

---

# Background information
This section introduces some background concepts which will be helpful to understand for the instructions and guidelines further below. 

### Payu and running experiments
ACCESS-ESM1.6 is run using the program [Payu](https://payu.readthedocs.io/en/stable/) via the same commands used for ACCESS-ESM1.5. If you are unfamiliar with running models with Payu or need a refresher, please see [this guide on running ACCESS-ESM1.5](https://docs.access-hive.org.au/models/run_a_model/run_access-esm/) for an introduction (new instructions for ESM1.6 are currently in preparation).

ACCESS-NRI staff will be available, via the ACCESS-Hive Forum, if you have any questions about running the model.

### Configurations and experiments
#### Configurations
A Payu *model configuration* contains the complete collection of model settings, configuration files, and paths to input and restart files required to run a model. Payu configurations for ACCESS-ESM1.6 are kept using branches the [access-esm1.6-configs](https://github.com/ACCESS-NRI/access-esm1.6-configs) GitHub repository, with `dev-` branches representing development versions of configurations and `release-` branches representing released configurations.

#### Experiments
When Payu runs a simulation, it keeps track of the configuration settings, input files, model executables, and restart files used for each run segment and records this information into a git commit in the Payu control directory. This information can be accessed later. For example, the configuration settings used for each segment of the ESM1.6 CMIP7 esm-piControl simulation are available to view [here](https://github.com/ACCESS-Community-Hub/access-esm1.6-dev-experiments/commits/dev-preindustrial%2Bemissions-14-04-26/). This sequence of commits are referred to as the Payu *runlogs*, and as a whole they form a Payu *experiment*.

On completion, ESM1.6 Payu experiments for the CMIP7 Assessment Fast Track will need to be uploaded to the [access-esm1.6-dev-experiments](https://github.com/ACCESS-Community-Hub/access-esm1.6-dev-experiments) GitHub repository.

Payu *configurations* and *experiments* both contain all the information required to run a model, and either can be used to start a simulation.

--- 

# Instructions and guidelines
## Cloning and running an experiment
In most cases, ACCESS-NRI and CSIRO will provide you with a branch on the [access-esm1.6-dev-experiments](https://github.com/ACCESS-Community-Hub/access-esm1.6-dev-experiments) GitHub repository which you can clone, run, and push the runlogs back to. 

For example, to clone the *example-experiment* [branch](https://github.com/ACCESS-Community-Hub/access-esm1.6-dev-experiments/tree/example-experiment), you would first load the payu module, and use:
```
payu clone git@github.com:ACCESS-Community-Hub/access-esm1.6-dev-experiments.git -B example-experiment <control directory name>
```

!!! warning
    If you are cloning an experiment which has been set up for you on the [access-esm1.6-dev-experiments](https://github.com/ACCESS-Community-Hub/access-esm1.6-dev-experiments) GitHub repository, it's important that you don't change the local branch name using the `-b <local-branch-name>` option from the `payu clone` command.*

Once the experiment has been cloned, you can `cd` into the control directory cloned in the command above and run it using the usual `payu run -n <n runs>` command.

!!! tip
    Some experiments will require a more complicated setup, such as scripts that need to be run before the initial simulation. Other experiments may need to be cloned from the [configuration repository](https://github.com/ACCESS-NRI/access-esm1.6-configs) rather than the [experiments repository](https://github.com/ACCESS-Community-Hub/access-esm1.6-dev-experiments). In these cases, ACCESS-NRI staff will provide you with specific instructions.



## Output syncing
Model outputs and restarts should be synced to a location on `/g/data` to prevent loss of data during the automatic cleanup of files on `/scratch`. We recommend configuring Payu to automatically sync the outputs and restarts to a location on `/g/data` by enabling the `sync` option in the `config.yaml`:

```diff
# Sync options for automatically copying data from ephemeral scratch space to
# longer term storage
sync:
-   enable: False # set path below and change to true
+   enable: True # set path below and change to true
    restarts: True
    base_path: <Location on /g/data>
```

With the above changes, Payu will create a new directory matching your experiment's name under the location specified by `base_path`. Outputs and restarts will then be copied to this location at the end of each run segment. For more information on automatic syncing, please see the [Payu documentation](https://payu.readthedocs.io/en/stable/config.html#:~:text=the%20PBS%20script.-,sync,-Sync%20archive%20to).

ACCESS-NRI and CSIRO staff will work with you to determine the best location for syncing your data.


## Output archiving
Output and restart files for ESM1.6 fast track experiments are being archived to the `p73` project. Write access to `p73` is restricted and so CSIRO team members will be in contact with you to organise a data copy upon your simulations' completion.


## Pushing completed experiments back to the repository
Once your simulations are complete, you'll need to push the runlogs back up to the [access-esm1.6-dev-experiments](https://github.com/ACCESS-Community-Hub/access-esm1.6-dev-experiments) GitHub repository using the following steps:

1.  First find the local branch name for each experiment by running the following command in the control directory:
    ```bash
    $ payu branch
    * Current Branch: <experiment-branch-name>
        experiment_uuid: 3e907528-b735-af72-b4v6-51c9b3l27960
    ```
2. Push the runlogs up to the repository:
   ```
   $ git push origin <experiment-branch-name>
   ```

!!! warning
    If your experiment was originally cloned from the [configuration repository](https://github.com/ACCESS-NRI/access-esm1.6-configs) rather than the [experiments repository](https://github.com/ACCESS-Community-Hub/access-esm1.6-dev-experiments), the above instructions won't apply. ACCESS-NRI staff will provide you with specific instructions in this case.


## Crashes, perturbing atmospheric restarts, and reproducibiliy

During the simulations you may run into model crashes. These can occur due to many different reasons including transient errors on Gadi and numerical instabilities in the model, and you're welcome to get in touch with ACCESS-NRI staff or add a [help request](https://forum.access-hive.org.au/t/support-faq-frequently-asked-questions/1021) to the ACCESS-Hive Forum for help with understanding the cause of a creash.

In general, we recommend the following approach for dealing with crashes:

First check the error logs for further information on the error, and try sweeping and rerunning using the payu commands from the experiment control directory:
```bash
$ payu sweep
$ payu run
```

If the same error occurs on the rerun, it may be due to a numerical instability and you can try perturbing the atmosphere restart file as a workaround. It's crucial to do this in a reproducible way and to keep a record of any perturbations applied. We recommend following the steps [outlined here](/inputs/restarts/#perturbing-an-atmospheric-restart-file), which will apply a reproducible perturbation and record it in the experiment runlogs.