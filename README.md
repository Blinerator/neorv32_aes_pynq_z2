# Introduction
This is the central repository containing build scripts and dependencies to build a NEORV32 RTL image targeting the PYNQ-Z2 board. This build flow is targeting a custom NEORV32 implementation, but can be modified for other version of the core as well. For details on re-configuring the NEORV32 core, refer to the [build.py](build.py) script.

# Dependencies
This build flow is intended for Vivado 2023.2, it is untested on other versions.

To fetch dependencies, run the following command in this directory:

`git clone git@github.com:Blinerator/neorv32.git --recurse-submodules`


