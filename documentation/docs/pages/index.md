
# Home

Welcome to the documentation for the [ACCESS-ESM1.6 model configurations](https://github.com/ACCESS-NRI/access-ESM1.6-configs)! 


## ACCESS-ESM1.6 Documentation Overview

See the navigation links on the left. Some reading tips, see:

 - [Contributing](/contributing) 
 - [Inputs](/inputs/Forcing-data-models) 
 - [Configuration choices/Configurations](/configurations/Overview/) 
 - [Infrastructure](/infrastructure/Architecture/) 

## access-esm1.6-configs Overview
ACCESS-ESM1.6 configurations are provided via branches in the [access-esm1.6-configs](https://github.com/ACCESS-NRI/access-esm1.6-configs) GitHub repository. The [access-esm1.6-configs](https://github.com/ACCESS-NRI/access-esm1.6-configs) repository contains several configurations using the following components:

- [MOM5](https://github.com/ACCESS-NRI/mom5) ocean model

All the configurations use the [Payu](https://payu.readthedocs.io/en/latest/) workflow management tool, and pre-built executables available on [NCI](https://nci.org.au/).

### Repository structure

The [`main`](https://github.com/ACCESS-NRI/access-esm1.6-configs/tree/main) branch does not store any model configurations, only documentation.

Each configuration in [github.com/ACCESS-NRI/access-esm1.6-configs](https://github.com/ACCESS-NRI/access-esm1.6-configs) repository is stored as a git branch. Most of the branches are named according to the following naming scheme:

`release-{scenario}[+{modifier}]`

where release signifies this is the release branch that is tested, versioned and ready for use, scenario is the base experimental design with optional modifiers. All configurations are assumed to be global extent with nominal 1 degree resolution.

Some examples of possible values of the specifiers:

- scenario: `historical`, `preindustrial`, `ssp126`
- modifier: `concentration`, `interactiveC`, `noLUC`

where scenario is typically a CMIP experiment identifier, concentration and interactiveC describe the CO2 cycling protocol, and noLUC is no land-use change.

#### Supported configurations

All available configurations are browsable under [the list of release branches](https://github.com/ACCESS-NRI/access-esm1.6-configs/branches/all?query=release-). There are currently no released configurations.


These configurations are under active development:
- [dev-preindustrial+concentrations](https://github.com/ACCESS-NRI/access-esm1.6-configs/tree/dev-preindustrial%2Bconcentrations)
- [dev-preindustrial+emissions](https://github.com/ACCESS-NRI/access-esm1.6-configs/tree/dev-preindustrial%2Bemissions)
- [dev-4xCO2+concentrations](https://github.com/ACCESS-NRI/access-esm1.6-configs/tree/dev-4xCO2%2Bconcentrations)
- [dev-1pctCO2](https://github.com/ACCESS-NRI/access-esm1.6-configs/tree/dev-1pctCO2)
- [dev-amip](https://github.com/ACCESS-NRI/access-esm1.6-configs/tree/dev-amip)

Where changes are made, they should be applied to all these branches (where relevant) by pull requests. These comparisons can assist with understanding differences between configurations:

- [dev-preindustrial+concentrations↔️dev-preindustrial+emissions
](https://github.com/ACCESS-NRI/access-esm1.6-configs/compare/dev-preindustrial+concentrations..dev-preindustrial+emissions
)

- [dev-preindustrial+concentrations↔️dev-4xCO2+concentrations
](https://github.com/ACCESS-NRI/access-esm1.6-configs/compare/dev-preindustrial+concentrations..dev-4xCO2+concentrations
)

- [dev-preindustrial+concentrations↔️dev-1pctCO2
](https://github.com/ACCESS-NRI/access-esm1.6-configs/compare/dev-preindustrial+concentrations..dev-1pctCO2
)



#### How to use this repository to run a model

All configurations use [payu](https://github.com/payu-org/payu) to run the model.

This repository contains many related experimental configurations to make support
and discovery easier. As a user it does not necessarily make sense to clone all the
configurations at once.

In most cases only a single experiment is required. If that is the case, choose which experiment and then run

```sh
git clone -b <experiment> https://github.com/ACCESS-NRI/access-esm1.6-configs <experiment>
```

and replace `<experiment>` with the branch name or tag of the experiment you wish to run.

[ACCESS-Hive](https://access-hive.org.au/) contains [detailed instructions for how to configure and run ACCESS models with `payu`](https://access-hive.org.au/models/run-a-model).

#### CI and Reproducibility Checks

This repository makes use of GitHub Actions to perform reproducibility checks on model config branches.


