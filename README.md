# Archaea Simulation

Wrapper definitions for simulation tools.

Motivation of creating this library is started with master thesis, departments of Computational
Science and Engineering and Architecture at Istanbul Technical University. 
Aim of thesis is to create scenarios for different environmental
solvers like EnergyPlus and OpenFOAM to run them parallely on Linux environment.
Preparation of these scenario files done by geometric [Archaea](https://github.com/archaeans/archaea) library.


## Focused Simulation Tools

- OpenFOAM: OpenFOAM requires stl geometries to run it's solvers
behind the scenes. (Pre-Alpha)
- EnergyPlus: EnergyPlus requires idf schema to run simulations. (MVP)
- UWG: Urban weather generator is a solver to calculate effects on urban microclimate.
It creates new .epw file for EnergyPlus simulations.

Main idea behind this work is to be experimental and didactic. 