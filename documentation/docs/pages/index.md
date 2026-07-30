
# Home

Welcome to the documentation for the [ACCESS-ESM1.6 model configurations](https://github.com/ACCESS-NRI/access-ESM1.6-configs)! 


## ACCESS-ESM1.6 Documentation Overview

See the navigation links on the left. Some reading tips, see:

 - [Contributing](/contributing) 
 - [Infrastructure](/infrastructure/building/) 

## access-esm1.6-configs Overview
ACCESS-ESM1.6 configurations are provided via branches in the [access-esm1.6-configs](https://github.com/ACCESS-NRI/access-esm1.6-configs) GitHub repository. The [access-esm1.6-configs](https://github.com/ACCESS-NRI/access-esm1.6-configs) repository contains several configurations using the following components:

- [MOM5](https://github.com/ACCESS-NRI/mom5) ocean model

All the configurations use the [Payu](https://payu.readthedocs.io/en/latest/) workflow management tool, and pre-built executables available on [NCI](https://nci.org.au/).

### Repository structure

The [`main`](https://github.com/ACCESS-NRI/access-esm1.6-configs/tree/main) branch does not store any model configurations, only documentation.

Each configuration in [github.com/ACCESS-NRI/access-esm1.6-configs](https://github.com/ACCESS-NRI/access-esm1.6-configs) repository is stored as a git branch. 

*Supported* configurations are named according to the following naming scheme:

`release-{scenario}`

where release signifies this is the release branch that is tested, versioned and ready for use. `{scenario}` is the CMIP7 experiment. 
Scenario names exactly match [CMIP7 experiment names](https://airtable.com/embed/apphXCUgASIeT6jCz/shrCs1cSWzQRV0v4i/tblbT6XAdQYOCMXu7).
All configurations are global with nominal 1 degree resolution. 

*Development* branches (`dev-{scenario}`) contain changes for future releases, and when merged into release branches create a release.

*Feature* branches contains tests, demonstrations and new features, and should be named using an issue number, scenario and other 
descriptors to disambiguate them.

#### Supported configurations

All supported configurations are browsable under [the list of release branches](https://github.com/ACCESS-NRI/access-esm1.6-configs/branches/all?query=release-).
The current releases are for the CMIP7 *piControl* and *historical* configurations with concentrations and emissions driven CO₂ forcings. 
Releases for _amip_ and some CMIP7 future scenarios are planned. 

#### Development configurations

The configurations under active development, have `dev-` branches - findable through this
[list](https://github.com/ACCESS-NRI/access-esm1.6-configs/branches/all?query=dev-).
It is recommended to use `release-` branches for experiments.

When changes are made, they should be applied to all `dev-` branches they are relevant to by pull requests. 

#### Archived configurations

There were some configurations previously under development that have now been archived.
These are available for reference as git [tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging).

These were `+CN` only, i.e. including the carbon and nitrogen cycles but excluding the phosphorus cycle in the land :

- [archive-amip+CN](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-amip%2BCN)
- [archive-1pctCO2-bgc+CN](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-1pctCO2-bgc%2BCN)
- [archive-1pctCO2-rad+CN](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-1pctCO2-rad%2BCN)
- [archive-1pctCO2+CN](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-1pctCO2%2BCN)
- [archive-4xCO2+concentrations+CN](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-4xCO2%2Bconcentrations%2BCN)
- [archive-flat10+CN](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-flat10%2BCN)
- [archive-historical+concentrations+CN](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-historical%2Bconcentrations%2BCN)
- [archive-preindustrial+concentrations+CN](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-preindustrial%2Bconcentrations%2BCN)
- [archive-preindustrial+emissions+CN](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-preindustrial%2Bemissions%2BCN)

These configurations were used for CMIP7 experiments:

- [archive-1pctCO2](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-1pctCO2)
- [archive-1pctCO2-bgc](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-1pctCO2-bgc)
- [archive-1pctCO2-rad](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-1pctCO2-rad)
- [archive-abrupt-4xCO2](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-abrupt-4xCO2)
- [archive-esm-flat10](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-esm-flat10)
- [archive-esm-flat10-cdr](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-esm-flat10-cdr)
- [archive-esm-flat10-zec](https://github.com/ACCESS-NRI/access-esm1.6-configs/releases/tag/archive-esm-flat10-zec)

If you need assistance to use git to update these configurations, please ask on the 
[ACCESS-Hive forum](https://forum.access-hive.org.au/new-topic?category=esm&tags=access-nri-help).

### Comparing configuration branches

GitHub's branch comparison view can be used to see exactly what differs between any two configurations.
This is useful, for example, to see how a `dev-*` configuration differs from the latest `release-*`
configuration it's based on, or how two configurations at different resolutions differ.

To compare any two branches, visit a URL of the form:

```
https://github.com/ACCESS-NRI/access-om3-configs/compare/{base-branch}..{compare-branch}
```

replacing `{base-branch}` and `{compare-branch}` with the names of the branches you want to compare.
This shows the `diff` between the `{base-branch}` and `{compare-branch}`. Lines shown in red are
only present in `{base-branch}` (i.e. absent from `{compare-branch}`) and lines shown in green are only
present in `{compare-branch}` (i.e. added relative to `{base-branch}`).

Note that the `..` produces a ["two-dot" diff](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-comparing-branches-in-pull-requests#three-dot-and-two-dot-git-diff-comparisons)
directly between the two refs, rather than the "three-dot" diff (against their merge base) that GitHub
uses for pull requests.

Tags or commit hashes can be used in place of branch names, which is useful for comparing
against a specific released version or commit, rather than the (potentially newer) tip
of a branch.

For example, to compare the `release-MC_25km_jra_iaf-1.0-beta` release tag with the `dev-MC_25km_jra_iaf`
branch, visit:

[`https://github.com/ACCESS-NRI/access-om3-configs/compare/release-MC_25km_jra_iaf-1.0-beta..dev-MC_25km_jra_iaf`](https://github.com/ACCESS-NRI/access-om3-configs/compare/release-MC_25km_jra_iaf-1.0-beta..dev-MC_25km_jra_iaf)

### How to use this repository to run a model

All configurations use [payu](https://github.com/payu-org/payu) to run the model.

This repository contains many related experimental configurations to make support
and discovery easier. As a user it does not necessarily make sense to clone all the
configurations at once.

In most cases only a single experiment is required. If that is the case, choose which experiment and then run

```sh
git clone -b <experiment> https://github.com/ACCESS-NRI/access-esm1.6-configs <experiment>
```

and replace `<experiment>` with the branch name or tag of the experiment you wish to run.

[ACCESS-Hive](https://access-hive.org.au/) contains [detailed instructions for how to configure and run ACCESS models with `payu`](https://access-hive.org.au/models/run_a_model).
