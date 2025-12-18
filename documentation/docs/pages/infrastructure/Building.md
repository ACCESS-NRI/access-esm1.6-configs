# Build infrastructure

Most users of ACCESS-ESM1.6 will not need to build the model. Released versions of the model are deployed by ACCESS-NRI to Gadi and available to users. If you require your own build of the model, you will find the required information on this page.

ACCESS-NRI is using [Spack](https://spack.io/), a build from source package manager designed for use with high performance computing. Spack already contains support for compiling thousands of common software packages. The build of ACCESS-ESM1.6 is managed from the [ACCESS-NRI/ACCESS-ESM1.6](https://github.com/ACCESS-NRI/ACCESS-ESM1.6) repository. 

ACCESS-ESM1.6 repository contains a Spack environment definition file, `spack.yaml`, that defines all the essential components of the ACCESS-ESM1.6 model, including exact versions. Spack automatically builds all the components and their dependencies, producing model component executables. Spack packages for the components in ACCESS-ESM1.6 are defined in the [Spack packages repository](https://github.com/ACCESS-NRI/access-spack-packages).

## Build your own version of ACCESS-ESM1.6

### Prerequisites

You need at least read permissions to all the model components of ACCESS-ESM1.6 in order to build the model. You need write permissions to any model component you need to modify. To request a higher level of permissions on one of the repositories, post a reply on [this ACCESS-Hive Forum topic](https://forum.access-hive.org.au/t/request-access-to-access-esm1-6-component-repositories/5709).

**Public repositories:**<br>
You have read access to these repositories by default. You need to request permissions if you need write access. 

- [github.com/ACCESS-NRI/cice5](https://github.com/ACCESS-NRI/cice5)
- [github.com/ACCESS-NRI/GFDL-generic-tracers](https://github.com/ACCESS-NRI/GFDL-generic-tracers)
- [github.com/ACCESS-NRI/FMS](https://github.com/ACCESS-NRI/FMS)
- [github.com/ACCESS-NRI/MOM5](https://github.com/ACCESS-NRI/MOM5)
- [github.com/ACCESS-NRI/mocsy](https://github.com/ACCESS-NRI/mocsy)

**Private repositories:**<br>
These repositories are covered by the UKMO's Momentum Partnership licence. You need to request permissions for either read or write access.

- [github.com/ACCESS-NRI/UM7](https://github.com/ACCESS-NRI/UM7) (private, access requires to be covered by the UKMO's Momentum Partnership licence)
- [github.com/ACCESS-NRI/GCOM4](https://github.com/ACCESS-NRI/GCOM4) (private, access requires to be covered by the UKMO's Momentum Partnership licence)

### Build ACCESS-ESM1.6

There are two ways to build ACCESS-ESM1.6 using the Spack infrastructure (on GitHub or locally) both with benefits and limitations. You can find the instructions for both methods on the ACCESS-Hive [Build a model pages](https://docs.access-hive.org.au/models/build_a_model/), replacing the examples with ACCESS-ESM1.6. We recommend users build the model following the GitHub workflow, i.e. [creating a prerelease](https://docs.access-hive.org.au/models/build_a_model/create_a_prerelease/). Since this method uses the infrastructure installed by ACCESS-NRI (and not user-installed software), it is a lot easier to get support. It also provides better tracking of the build and shareability of the build (all ACCESS-ESM1.6 users will have access to the pre-release).
