# Build infrastructure

Most users of ACCESS-ESM1.6 will not need to build the model. Released versions of the model are deployed by ACCESS-NRI to Gadi and available to users. If you require your own build of the model, typically because you need to modify one or several model components, you will find the required information on this page.

ACCESS-NRI is using [Spack](https://spack.io/), a build from source package manager designed for use with high performance computing. Spack already contains support for compiling thousands of common software packages. 

## Software structure

ACCESS-ESM1.6 being a Earth System model, it is constituted of several model components, each residing in its own repository on GitHub. In addition, some model components need other utilities at compilation time that are stored in separate repositories. This results in a complex software structure involving a large number of repositories:

- deployment repository: 
    - [ACCESS-NRI/ACCESS-ESM1.6](https://github.com/ACCESS-NRI/ACCESS-ESM1.6)
- model components:
    - [ACCESS-NRI/cice5](https://github.com/ACCESS-NRI/cice5)
    - [ACCESS-NRI/GFDL-generic-tracers](https://github.com/ACCESS-NRI/GFDL-generic-tracers)
    - [ACCESS-NRI/MOM5](https://github.com/ACCESS-NRI/MOM5)
    - [ACCESS-NRI/UM7](https://github.com/ACCESS-NRI/UM7)
    - [CABLE-LSM/CABLE](https://github.com/CABLE-LSM/CABLE)
- other software:
    - [ACCESS-NRI/FMS](https://github.com/ACCESS-NRI/FMS)
    - [ACCESS-NRI/mocsy](https://github.com/ACCESS-NRI/mocsy)
    - [ACCESS-NRI/GCOM4](https://github.com/ACCESS-NRI/GCOM4)

!!! note

    The _UM7_ and _GCOM4_ repositories are private because these software are not open-source. They are covered by the UKMO's Momentum Partnership licence. To gain access to these repositories, please request an invitation via [this ACCESS-Hive forum topic](https://forum.access-hive.org.au/t/request-access-to-access-esm1-6-component-repositories/5709).

## Building ACCESS-ESM1.6 using the deployment infrastructure

This is the recommended method to build ad-hoc versions of ACCESS-ESM1.6 because it does not require users to have access to all the repositories, it handles the build automatically and it provides traceability and shareability of the deployment.

This method is explained on the ACCESS-Hive page for [creating pre-releases and releases](https://docs.access-hive.org.au/models/build_a_model/create_a_prerelease/) of ACCESS models. For ACCESS-ESM1.6, you will need _write permissions_ on the [ESM1.6 deployment repository](https://github.com/ACCESS-NRI/ACCESS-ESM1.6) and on any model component you need to modify. Request these permissions via this [ACCESS-Hive forum topic](https://forum.access-hive.org.au/t/request-access-to-access-esm1-6-component-repositories/5709).

!!! warning

    This method to build the model only works if your modifications are committed in branches of the model repositories listed in the [software structure](#software-structure). This method can not be used if your modifications sit in a fork of one of the repositories.

## Local build of ACCESS-ESM1.6

The Spack infrastructure allows you to create your own local build on _Gadi_ for ACCESS-ESM1.6. Once setup, this might be faster than using the deployment infrastructure, especially when you want a lot of small incremental builds during development. It also allows to build the model with debugging symbols for the debugger. 

However, this method has several drawbacks. It requires users to install the Spack software which can make it harder for ACCESS-NRI to provide support. It requires users to have at least _read permissions_ on all the repositories required by ACCESS-ESM1.6 (see [Software structure](#software-structure)). It builds the model in the user space on _Gadi_ thus limiting the shareability of the build and consuming a potentially non-insignificant amount of inodes. Finally, contrary to the deployment infrastructure, it does not provide an easy way to access several test builds from the same model component branch at the same time.

This method is explained on the ACCESS-Hive page for [modifying an ACCESS model's source code](https://docs.access-hive.org.au/models/build_a_model/build_source_code/). 