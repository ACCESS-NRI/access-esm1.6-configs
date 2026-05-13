# ACCESS-ESM1.6 Model Configurations

## About

This repository contains standard global configurations for ACCESS-ESM1.6, the ACCESS Coupled Earth System Model. See the [ACCESS-ESM1.6 configuration docs](https://access-nri.github.io/access-esm1.6-configs/) for more information on the supported configurations and how to run the model.

## Conditions of use

The developers of ACCESS-ESM1.6 request that users of these model configurations

1. Cite https://doi.org/10.1071/ES19035A model description paper. An new paper for ACCESS-ESM1.6 is in preperation.
2. Follow the [guidelines for acknowledging ACCESS-NRI](https://www.access-nri.org.au/resources/acknowledging-us/) and also acknowledge the ongoing science developments led by CSIRO, by including a statement such as:
"This research used the ACCESS-ESM1.6 model infrastructure provided by ACCESS-NRI, which is enabled by the Australian Government’s National Collaborative Research Infrastructure Strategy (NCRIS). Science development of ACCESS-ESM1.6 was led by CSIRO with support from the Australian Government's National Environmental Science Program Climate Systems Hub."
3. Have a Met Office Science Repository Service (MOSRS) account as described on [ACCESS-Hive Docs](https://docs.access-hive.org.au/models/run_a_model/run_access-esm/#prerequisites).


## CI and Reproducibility Checks

This repository makes use of GitHub Actions to perform reproducibility checks on model config branches.

### Config Branches

Config branches are branches that store model configurations of the form: `release-<config>` or `dev-<config>`, for example: `release-historical+concentration`. For more information on creating your own config branches, or for understanding the PR process in this repository, see the [CONTRIBUTING.md](CONTRIBUTING.md).

### Config Tags

Config tags are specific tags on config branches, whose `MAJOR.MINOR` version compares the reproducibility of the configurations. Major version changes denote that a particular config tag breaks reproducibility with tags before it, and a minor version change does not. These have the form: `release-<config>-<tag>`, such as `release-historical+concentration-1.2`.

So for example, say we have the following config tags:

* `release-historical+concentration-1.0`
* `release-historical+concentration-1.1`
* `release-historical+concentration-2.0`
* `release-historical+concentration-3.0`

This means that `*-1.0` and `*-1.1` are configurations for that particular experiment type that are reproducible with each other, but not any others (namely, `*-2.0` or `*-3.0`).

`*-2.0` is not reproducible with `*-1.0`, `*.1.1` or `*-3.0` configurations.

Similarly, `*-3.0` is not reproducible with `*-1.0`, `*-1.1` or `*-2.0`.

### Checks

These checks are in the context of:

* PR checks: In which a PR creator can modify a config branch, create a pull request, and have their config run and checked for reproducibility against a 'ground truth' version of the config.
* Scheduled checks: In which config branches and config tags that are deemed especially important are self-tested monthly against their own checksums.

More information on submitting a Pull Request and on the specifics of this pipeline can be found in the [CONTRIBUTING.md](./.github/CONTRIBUTING.md) and [README-DEV.md](./README-DEV.md) respectively.

For more information on the manually running the pytests that are run as part of the reproducibility CI checks, see
[model-config-tests](https://github.com/ACCESS-NRI/model-config-tests/).

## Automated Cherry Picking

There is a workflow which enables semi-automated cherry-picking from one branch into another, using the !cherry-pick keyword in a pull-request. This is useful when a change needs to be applied across multiple branches.

For example, if a pull-request changes `dev-preindustrial+concentrations`, to apply the change to `dev-4xCO2+concentrations`:
- First finalise and merge the pull-request into `dev-preindustrial+concentrations`
- Second, as a standalone comment in the pull-request, use the keyword as follows:
    ` !cherry-pick <commit> into <branch> `

<commit> must exist in `dev-preindustrial+concentrations`. This can be one or multiple commit hashes seperated by spaces.
<branch> would be `dev-4xCO2+concentrations` in this example

This will attempt to make a new pull-request with the request commit(s), and leave a comment on the initial-pull request with the outcome.
