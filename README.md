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
├── MODSIMNodes.xlsx         # MODSIM Node mapping   
├── README.md  
├── LICENSE  

---

## Input Requirements

Scenario CSV files:
- No header row  
- First two columns: year, month  
- Remaining columns: daily station data, inflow/demand  

MODSIMNodes.xlsx must include:
- MODSIM node name  
- station index  
- multiplier (if applicable)  

MODSIM-DSS model:
- .xy and .exe files

---

## Outputs

For each scenario:
- A working MODSIM model is created  
- Simulation is executed  
- Selected outputs are saved, including:  
  - [modelname]TargetOutput.csv  
  - [modelname]RES_STOROutput.csv  

---

## Important Notes

- Users must provide their own:
  - MODSIM executable
  - input datasets  

---

## Citation

TBD
