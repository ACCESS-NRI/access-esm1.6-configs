# Deployment

ACCESS-ESM1.6 is deployed automatically when a new version of the spack.yaml file is committed to the `main` branch or a dedicated `backport/VERSION` branch of the [ACCESS-NRI/ACCESS-ESM1.6](https://github.com/ACCESS-NRI/ACCESS-ESM1.6) repository. 

ACCESS-ESM1.6 is deploed in /g/data/vk83. It is necessary to be a member of vk83 project to use ACCESS-NRI deployments of ACCESS-ESM1.6. All deployed versions are available as modules to load. To check all the released versions of ACCESS-ESM1.6 on Gadi:

```
module use /g/data/vk83/modules
module avail access-esm1p6
```

For users of ACCESS-ESM1.6 model configurations released by ACCESS-NRI, the exact location of the ACCESS-ESM1.6 model executables is not required. Model configurations will be updated with new model releases when necessary.

## Release information

The deployment process creates a GitHub release with the same tag as the deployed module. All releases are available under the [Releases page](https://github.com/ACCESS-NRI/ACCESS-ESM1.6/releases). Each release has a changelog and meta-data with detailed information about the build and deployment, including:

- paths on Gadi to all executables built in the deployment process (spack.location)
- a spack.lock file, which is a complete build provenance document, listing all the components that were built and their dependencies, versions, compiler version, build flags and build architecture
- the environment spack.yaml file used for deployment