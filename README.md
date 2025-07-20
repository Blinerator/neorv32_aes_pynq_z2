# Introduction
This is the central repository containing build scripts and dependencies to build a NEORV32 RTL image targeting the PYNQ-Z2 board. This build flow is targeting a custom NEORV32 implementation, but can be modified for other version of the core as well. For details on re-configuring the NEORV32 core, refer to the [build.py](build.py) script.

# Dependencies
This build flow is intended for Vivado 2023.2, it is untested on other versions.

To clone down this repository and all dependencies, run this command:

`git clone git@github.com:Blinerator/neorv32_aes_pynq_z2.git --recurse-submodules`

Or, if the project has already been cloned down, run this command to initialize, fetch, and checkout submodules:

`git submodule update --init --recursive`

# Generating a bitstream
The build.py script generates handles building the project from start to finish. It creates a Vivado project in the syn/ directory; if the block diagram needs to be changed, it should be modified in the Vivado GUI and then saved to syn/block_design.tcl. It will be automatically sourced on the next build.

To run a build, execute the following in this directory:

`py ./build.py`
