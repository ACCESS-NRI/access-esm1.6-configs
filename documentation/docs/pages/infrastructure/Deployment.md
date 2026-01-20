# Deployment

All released versions of ACCESS-ESM1.6 come with a pre-deployed build on _Gadi_. Deployed builds are stored under the project `vk83` (hence requiring [membership to this project](https://my.nci.org.au/mancini/project/vk83/join) for access). You can see all deployed builds via:

```bash
module use /g/data/vk83/modules
module avail access-esm1p6
```

There are development releases (identified with a `dev_` prefix to the date tag) and full releases (identified with only a date tag). We recommend new users start with the newest full release (i.e., with the most recent date tag). 

These builds are optimised for the Sapphire-Rapid hardware from Intel (i.e., the *normalsr* queue), and may not run on Cascade-Lake (i.e., the *normal* queue) or older hardware.

The ACCESS-ESM1.6 model configurations released by ACCESS-NRI are setup to use the proper model release and will be updated when necessary.


## Release information

The deployment process creates a GitHub release with the same tag as the deployed module. All releases are available under the [Releases page](https://github.com/ACCESS-NRI/ACCESS-ESM1.6/releases). Each release has a changelog and meta-data with detailed information about the build and deployment, including:

- paths on Gadi to all executables built in the deployment process (spack.location)
- a spack.lock file, which is a complete build provenance document, listing all the components that were built and their dependencies, versions, compiler version, build flags and build architecture
- the environment spack.yaml file used for deployment

## Deployment process

The deployment is managed via GitHub Actions that are triggered when a new version of the spack.yaml file is committed to the `main` branch or a dedicated `backport/VERSION` branch of the [ACCESS-NRI/ACCESS-ESM1.6](https://github.com/ACCESS-NRI/ACCESS-ESM1.6) repository. 

No manual deployments will be accepted.
