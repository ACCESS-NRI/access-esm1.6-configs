# TEMPLATE for Model Configuration Repositories

A template repository for model configurations utilizing the `ACCESS-NRI/model-config-tests` CI infrastructure

> [!NOTE]
> Feel free to replace this README with information on the model configurations once the TODOs have been ticked off. An example README.md is in the last section

## Things TODO to get your configs repo ready

### Settings

#### Repository Settings

Appropriate branch protections (or rulesets) should be set up on `main`, `release-*` and `dev-*` branches.

#### Repository Secrets/Variables

There are a few repository secrets and variables that need to be set:

* `secrets.GH_COMMIT_CHECK_TOKEN` used to allow checks to run on workflow-generated commits.
* `secrets.GH_FORCE_PUSH_TOKEN` used to bypass branch protections for committing checksums to `release-*` branches.
* `vars.CI_JSON_SCHEMA_VERSION`: the version of the schema for the `config/ci.json` configuration file. Possible versions are found [in the `ACCESS-NRI/schema` repository here](https://github.com/ACCESS-NRI/schema/tree/main/au.org.access-nri/model/configuration/ci).

#### Environment Secrets/Variables

> [!IMPORTANT]
> These Environments MUST be created in your `<model>-configs` repository, otherwise the linked reusable workflows will not have the information required to connect to a given deployment target.

GitHub Environments are sets of variables and secrets that have more security requirements for their use. For example, they can require that a user or team must sign off on jobs that use a given environment, because it makes use of allocated supercomputer time, for example.

We at present require two environments per deployment target with the same information - one that is used with the `ci.yml` and `schedule.yml` workflows, and a protected one that is used by the user-dispatchable `generate-initial-checksums.yml` workflow. For a deployment target `SUPERCOMPUTER`, we usually call these `SUPERCOMPUTER` and `SUPERCOMPUTER Initial Checksum` respectively.

Regarding the secrets and variables that must be created:

* `secrets.SSH_HOST`: The deployment location SSH Host
* `secrets.SSH_HOST_DATA`: The deployment location SSH Host for data transfer (may be the same as `SSH_HOST`)
* `secrets.SSH_KEY`: A SSH Key that allows access to the above `HOST`/`HOST_DATA`
* `secrets.SSH_USER`: A Username to login to the above `HOST`/`HOST_DATA`
* `vars.DEPLOYMENT_TARGET`: Name of the deployment target for logging purposes (ex. `Supercomputer`)
* `vars.EXPERIMENTS_LOCATION` - directory on the deployment target that will contain all the experiments used during testing of reproducibility across multiple runs of this workflow (ex. `/scratch/some/directory/experiments`)

### File Modifications

#### In `config/ci.json`

This file contains configuration information on the types of pytest markers to run for different styles of test, as well as the version of Python and the overall [`model-config-tests` package](https://github.com/ACCESS-NRI/model-config-tests). It contains sensible defaults in case one does not specify `markers`, `python-version` or `model-config-tests-version`.

There are two levels of defaults. There's a default at test type level which is useful for defining test markers - this selects certain pytests to run in `model-config-tests`. There is an outer global default, which is used if a property is not defined for a given branch/tag, and it is not defined for the test default. The `parse-ci-config` action applies the fall-back default logic.

Hence, one will need to modify this file as configuration tags are added (for `scheduled` checks) or new markers are added (for `reproducibility`/`qa` checks).

For example, if one wants to add scheduled checks with the default markers for the config tag `release-1deg_jra55_iaf-2.0`, you would add the following to the `scheduled` section in `config/ci.json`:

```json
{
    # ...
    "scheduled": {
        "release-1deg_jra55_iaf-2.0": {},
        # ...
    }
}
```

If you wanted to add the tests from some new marker `other`, it would look like so:

```json
{
    # ...
    "scheduled": {
        "release-1deg_jra55_iaf-2.0": {
            "markers": "other or checksum"
        },
        # ...
    }
}
```

Note that the `default` at any level can be modified to your own liking.

#### In `.github/workflows/schedule.yml`

Check the `on.schedule.cron` trigger - currently it runs on the first day of every month. Adjust as required.

#### In `.github/workflows/generate-initial-checksums.yml`

Check the GitHub Environment specified in `jobs.generate-checksums.with.environment-name`. It is currently `Gadi Initial Checksum`. Adjust the name depending on the deployment target.

#### In `.github/workflows` More Generally

As [noted earlier](#environment-secretsvariables), one must have created the appropriate GitHub Environments in order for all the linked reusable workflows to work correctly.

Note the `jobs.*.secrets:inherit` sections on almost all of the jobs in each workflow - it is explicitly inheriting the secrets and variables from the GitHub Environments that you have created in _your_ repository, _not_ the repository that contains the reusable workflows!

## Example README.md

> [!NOTE]
> Even though this is an example, there are some fill-in-the-blanks in `<these>`. Adjust to your specific flavour of model configuration repository.

## About

This repo contains standard global configurations for `<MODEL>`.

This is an "omnibus repository": it contains multiple related configurations, and each
configuration is stored in a separate branch.

Branches utilise a naming scheme of `<some kind of scheme like{resolution}_{atmosforcing}_{forcingmode}[_{option}]>`.

## Supported configurations

All available configurations are browsable under [the list of branches](https://github.com/ACCESS-NRI/<model>-configs/branches) and should also be listed below:

| Branch | Configuration Description |
| ------ | ------------------------- |
| [`release-example-configuration`](https://github.com/ACCESS-NRI/<model>-configs/tree/release-example-configuration) | A model |

There are more detailed notes contained in the respective branches for each configuration.

More supported configurations will be added over time.

## How to use this repository to run a model

All configurations use [payu](https://github.com/payu-org/payu) to run the model.

This repository contains many related experimental configurations to make support
and discovery easier. As a user it does not necessarily make sense to clone all the
configurations at once.

In most cases only a single experiment is required. If that is the case choose which experiment and then run

```sh
git clone -b <experiment> https://github.com/ACCESS-NRI/model-configs/ <experiment>
```

and replace `<experiment>` with the branch name or tag of the experiment you wish to run.

[ACCESS-Hive](https://access-hive.org.au/) contains [detailed instructions for how to configure and run `<MODEL>` with `payu`](https://access-hive.org.au/models/run-a-model).

## CI and Reproducibility Checks

This repository makes use of GitHub Actions to perform reproducibility checks on model config branches.

### Config Branches

Config branches are branches that store model configurations of the form: `release-<config>` or `dev-<config>`, for example: `release-1deg_jra55_iaf`. For more information on creating your own config branches, or for understanding the PR process in this repository, see the [CONTRIBUTING.md](CONTRIBUTING.md).

### Config Tags

Config tags are specific tags on config branches, whose `MAJOR.MINOR` version compares the reproducibility of the configurations. Major version changes denote that a particular config tag breaks reproducibility with tags before it, and a minor version change does not. These have the form: `release-<config>-<tag>`, such as `release-1deg_jra55_iaf-1.2`.

So for example, say we have the following config tags:

* `release-1deg_jra55_iaf-1.0`
* `release-1deg_jra55_iaf-1.1`
* `release-1deg_jra55_iaf-2.0`
* `release-1deg_jra55_iaf-3.0`

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

## Conditions of use

`<NOTE CONDITIONS OF USE>`
