# Build infrastructure

Most users of ACCESS-ESM1.6 will not need to build the model. Released versions of the model are deployed by ACCESS-NRI to Gadi and available to users. If you require your own build of the model, you will find the required information on this page.

ACCESS-NRI is using [Spack](https://spack.io/), a build from source package manager designed for use with high performance computing. Spack already contains support for compiling thousands of common software packages. The build of ACCESS-ESM1.6 is managed from the [ACCESS-NRI/ACCESS-ESM1.6](https://github.com/ACCESS-NRI/ACCESS-ESM1.6) repository. 

ACCESS-ESM1.6 repository contains a Spack environment definition file, `spack.yaml`, that defines all the essential components of the ACCESS-ESM1.6 model, including exact versions. Spack automatically builds all the components and their dependencies, producing model component executables. Spack packages for the components in ACCESS-ESM1.6 are defined in the [Spack packages repository](https://github.com/ACCESS-NRI/access-spack-packages).

## Build your own version of ACCESS-ESM1.6

In order to build your own version of ACCESS-ESM1.6, you will need read access to the following repositories: 

- https://github.com/ACCESS-NRI/cice5
- https://github.com/ACCESS-NRI/GFDL-generic-tracers
- https://github.com/ACCESS-NRI/UM7 (private, access requires to be covered by the UKMO's Momentum Partnership licence)
- https://github.com/ACCESS-NRI/FMS
- https://github.com/ACCESS-NRI/MOM5
- https://github.com/ACCESS-NRI/GCOM4 (private, access requires to be covered by the UKMO's Momentum Partnership licence)
- https://github.com/ACCESS-NRI/mocsy

There are two ways to build ACCESS-ESM1.6 using the Spack infrastructure (on GitHub or locally) both with benefits and limitations.

You can find the instructions for both methods on the ACCESS-Hive [Build a model pages](https://docs.access-hive.org.au/models/build_a_model/), replacing the examples with ACCESS-ESM1.6.
