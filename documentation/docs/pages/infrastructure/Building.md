# Build infrastructure

ACCESS-NRI is using [Spack](https://spack.io/), a build from source package manager designed for use with high performance computing. Spack already contains support for compiling thousands of common software packages. The build of ACCESS-ESM1.6 is managed from the [ACCESS-NRI/ACCESS-ESM1.6](https://github.com/ACCESS-NRI/ACCESS-ESM1.6) repository. 

ACCESS-ESM1.6 repository contains a Spack environment definition file, `spack.yaml`, that defines all the essential components of the ACCESS-ESM1.6 model, including exact versions. Spack automatically builds all the components and their dependencies, producing model component executables. Spack packages for the components in ACCESS-ESM1.6 are defined in the [Spack packages repository](https://github.com/ACCESS-NRI/access-spack-packages).

## Build your own version of ACCESS-ESM1.6

If you need to modify the source code for ACCESS-ESM1.6, you will need to use the Spack infrastructure to create your own build. There are two ways to do so (on GitHub or locally) both with benefits and limitations.

You can find the instructions for both methods on the ACCESS-Hive [Build a model pages](https://docs.access-hive.org.au/models/build_a_model/), replacing the examples with ACCESS-ESM1.6.
