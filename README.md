# ACCESS-ESM with **payu**

## Quickstart Guide

Get payu:

    module use /g/data3/hh5/public/modules
    module load conda/analysis3

Get some global CABLE files:

    test -d $HOME/CABLE-AUX-1.4 || cp -r ~access/data/ACCESS_CMIP5/CABLE-AUX-1.4 $HOME/

Create a directory in which to keep the model configurations:

    mkdir -p ~/access-esm
    cd ~/access-esm
    git clone https://github.com/coecms/access-esm-amip
    cd access-esm-amip

Run the model:

    payu run

Check the output:

    ls archive/

The default configuration is a 1 year per model run. To run the model for, say, 25 years:

    payu run -n 25

With default settings, 1 model year cost is ~ 1100 SU, with a walltime of 1 hour 20 minutes

**Note:**
We have noticed that some modules interfere with the git commands, for example `matlab/R2018a`.
If you are running into issues during the installation, it might be a good idea to `module purge` first before starting again.

## Understanding **payu**

**payu** was designed to help users of the NCI system run climate models.
It was initially created for MOM, but has been adapted for other models,
including coupled ones.

The aim of **payu** is to make it easy and intuitive to configure and run the models.

**payu** knows certain models and how to run them. Adding more models needs additions to the **payu** sources.
This will not be part of this document.

### Terms

To understand **payu**, it helps to distinguish certain terms:

-   The **laboratory** is a directory where all parts of the model are kept.
    It is typically in the user's short directory, usually at `/short/$PROJECT/$USER/<MODEL>`
-   The **Control Directory** is the directory where the model configuration is
    kept and from where the model is run.
-   The **work** directory is where the model will actually be run.
    It is typically a subdirectory of the Laboratory.
    Submodels will have their own subdirectories in the work directory, named
    after their name in the master configuration file.
    It is ephemeral, that means payu will clean it up after the run.
-   The **archive** directory is where **payu** puts all output files after each run.

The **work** and **archive** directories will be automatically created by **payu**.

### The master configuration file

In the Control Directory, the file `config.yaml` is the master control file.
Examples of what is configured in this file are:

-   The actual model to run.
-   Where to find the model binaries and configurations
-   What resources to request from the scheduling system (PBS)
-   Links to the laboratory
-   Start date and run length per submission pf the model

The model configuration files are typically in subdirectories of the Control Directory,
the location of which is referenced in the master control file.
Since the models itself do need different ways to set up the model, the contents of these subdirectories will differ between different models.

## Understanding ACCESS-ESM

ACCESS (Australian Community Climate and Earth System Simulator) is a Coupled Climate Model.

Normally, the ESM 1.5 subversion of ACCESS specifically contains these models:

| Component  | Model      | Version |
| ---------- | ---------- | ------- |
| Atmosphere | UM-HG3     | 7.3     |
| Ocean      | MOM        | 5       |
| Sea Ice    | CICE       | 4.1     |
| Land       | CABLE      | 2.2.4   |
| Coupler    | OASIS-MCT  | 3.5     |

but for the AMIP case, only the UM is used.

~~Pre-compiled executables for these models are available on raijin at
`/short/public/access-esm/payu/bin/csiro/`.~~

## Setting up ACCESS-ESM with **payu**

### The pre-conditions

On `gadi`, first make sure that you have access to our modules.
This can most easily been done by adding the line

    module use /g/data3/hh5/public/modules

to your `~/.profile`, then logging back in. Then all you have to do is

    module load conda

to load the **payu** module.

as **payu** will use git to keep track of all configuration changes automatically.

### Setting up the control directory

Create a directory in your home directory to keep all the Control Directories you might want.

    mkdir ~/access-esm
    cd ~/access-esm

The cable submodel needs some files in your home directory at a specific location. 
Use this command to ensure they're there:

    test -d $HOME/CABLE-AUX-1.4 || cp -r ~access/data/ACCESS_CMIP5/CABLE-AUX-1.4 $HOME/

Then clone the most recent version of the ACCESS-ESM control directory:

    git clone https://github.com/coecms/access-esm-amip
    cd access-esm-amip

(Note: Currently we only have the historical model set up, other versions will follow later.)

### Setting up the Master Configuration file.

Open the `config.yaml` file with your preferred text editor.

Let's have a closer look at the parts:

    jobname: historical
    queue: normal
    walltime: 20:00:00

These are settings for the PBS system. Name, walltime and queue to use.

    # note: if laboratory is relative path, it is relative to /short/$PROJECT/$USER
    laboratory: access-esm

The location of the laboratory. At this point, **payu** can not expand shell environment variables (it's in our TO-DO), so as a work-around, if you use relative paths, it will be relative to your default short directory.

In this default configuration, it will be in `/short/$PROJECT/$USER/access-esm`.
But you can also hard-code the full path, if you want it somewhere different.

    model: um
    ncpus: 192
    exe: /g/data/access/payu/access-esm/bin/coe/amip/um7.3x
    input:
    - /g/data/access/payu/access-esm/input/amip


Each submodel has
- the **model** to know which driver to use
- the number of CPUs that this model should receive (**ncpus**)
- the location of the executable to use (**exe**)
- one or more locations for the **input** files.

The **name** is more than a useful reminder of what the model is.
**payu** expects this submodel's configuration files in a subdirectory with that name.

    restart: /g/data/access/payu/access-esm/restart/amip

This is the location of the warm restart files.
**payu** will use the restart files in there for the initial run.

    calendar:
        start:
            year: 1978
            month: 1
            days: 1

        runtime:
            years: 1
            months: 0
            days: 0

Here is the start date, and the runtime **per run**.
The total time you want to model is `runtime` * `number of runs`

    runspersub: 1

This `runspersub` feature is a nifty tool to allow you to bundle several runs into a single submission for the PBS queue.

Let's have an example: Say you told **payu** to make 7 runs with the above setting.
Each run would have a runtime of 1 year. So in the first submission it would run the model 5 times, to model years 101 through 105 respectively.

Then it would automatically resubmit another pbs job to model years 106 and 107, and then end.

### Setting up the Atmosphere Submodel

There are many configuration files, but I want to note the `um_env.py`.
This file is used to set environment variables for the UM.
The UM driver of **payu** will look for this file and add these definitions to the environment when it runs the model.

Most other configuration settings are made using the `namelists` file.


## Running the Model

If you have set up the modules system to use the `/g/data3/hh5/public/modules` folder, a simple `module load conda/analysis3-unstable` should give you access to the **payu** system.

From the control directory, type

    payu setup

This will prepare a the model run based on the configuration of the experiment.
It will setup `work` and `archive` directories and link to them from within the
configuration directory.
You don't have to do that, as the run command also sets it up, but it helps to check for errors.

    payu sweep

This command removes the `work` directory again, but leaves the `archive`.

Finally,

    payu run

will submit a single run to the queue.
It will start from the beginning (as indicated by the `start` section in the `config.yaml`) if it has not run before.

To automatically submit several runs (and to take advantage of the `runspersub` directive), you use the `-n` option:

    payu run -n 7

## Finding the Output

The output is automatically copied to the `archive/outputXXX` directories.

**Warning**: This directory is a link to your laboratory (probably on scratch), so while it might *seem* that the output files are created twice, they are not. Deleting them from one location also removes them from the other. Do not do that if you want to keep the data.
