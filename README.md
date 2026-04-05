# Automated MODSIM-DSS Runner

A Python-based workflow for preparing (importing daily inflow and demand scenarios) and executing (Parallel Run) MODSIM-DSS models.

---

## Overview

This project was developed to support scenario-based hydropower system analysis. It automates the full simulation pipeline by:

- Converting daily inflow scenario data into MODSIM-compatible format
- Mapping station data to MODSIM nodes
- Updating MODSIM `.xy` model files dynamically
- Running MODSIM simulations in parallel batches
- Extracting and organizing key output results

---

## Repository Structure

Automated-MODSIM-DSS-Run/
├── BatchRunner.py           # Multi-run
├── Run.py                   # Main execution script    
├── ExtractData.py           # Converts inflow and demand CSV data to MODSIM format  
├── ModifyMODSIM.py          # Updates MODSIM .xy file  
├── RunMODSIM_Single.py      # Executes MODSIM model  
├── MODSIMNodes.xlsx         # MODSIM-DSS Node mapping   
├── README.md  
├── LICENSE  

---

## Input Requirements

Scenario CSV files:
- No header row  
- First two columns: year, month  
- Remaining columns: station data  

MODSIMNodes.xlsx must include:
- MODSIM node name  
- station index  
- multiplier (if applicable)  

---

## Outputs

For each scenario:
- A working MODSIM model is created  
- Simulation is executed  
- Selected outputs are saved, including:  
  - MB_HydroSimHydroTargetOutput.csv  
  - MB_HydroSimRES_STOROutput.csv  

---

## Important Notes

- This repository does NOT include MODSIM software  
- Users must provide their own:
  - MODSIM executable  
  - base model files  
  - input datasets  

---

## Citation

TBD
