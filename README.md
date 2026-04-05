# MODSIM Batch Scenario Runner

A Python-based workflow for preparing, executing, and post-processing batch MODSIM simulations using daily scenario inputs. This repository enables automated large-scale hydropower system simulations by integrating data preprocessing, model updating, parallel execution, and result extraction.

---

## Overview

This project was developed to support scenario-based hydropower system analysis, particularly for large-scale systems such as the Manitoba Hydro network. It automates the full simulation pipeline by:

- Converting daily inflow scenario data into MODSIM-compatible format
- Mapping station data to MODSIM nodes
- Updating MODSIM `.xy` model files dynamically
- Running MODSIM simulations in parallel batches
- Extracting and organizing key output results

The workflow is designed for computational efficiency, reproducibility, and scalability across many scenarios.

---

## Key Features

- Automated workflow from raw CSV inputs to final simulation outputs  
- Parallel execution using multiprocessing to reduce runtime  
- Flexible batch control for large ensembles of scenarios  
- Custom node mapping using an external Excel file  
- Selective output extraction to reduce storage requirements  
- Modular design for easy modification and extension  

---

## Repository Structure

modsim-batch-runner/
├── Run.py                    # Main batch execution script  
├── BatchRunner.py           # Multi-run orchestrator  
├── ExtractData.py           # Converts CSV data to MODSIM format  
├── ModifyMODSIM.py          # Updates MODSIM .xy file  
├── RunMODSIM_Single.py      # Executes MODSIM model  
├── MODSIMNodes.xlsx         # Node mapping (optional / if shareable)  
├── requirements.txt         # Python dependencies  
├── README.md  
├── LICENSE  

---

## Workflow Description

1. Data Extraction (ExtractData.py)  
   - Reads raw daily scenario CSV files  
   - Maps station columns to MODSIM nodes  
   - Applies unit conversions and multipliers  
   - Outputs MODSIM-ready time series  

2. Model Update (ModifyMODSIM.py)  
   - Parses MODSIM `.xy` file  
   - Replaces time series blocks for inflow and demand nodes  
   - Maintains MODSIM file structure integrity  

3. Simulation Execution (RunMODSIM_Single.py)  
   - Runs the MODSIM executable  
   - Tracks execution time  
   - Captures errors if they occur  

4. Batch Processing (Run.py)  
   - Processes multiple scenarios  
   - Runs simulations in parallel batches  
   - Manages working directories  

5. Multi-Run Automation (BatchRunner.py)  
   - Executes multiple scenario groups  
   - Organizes outputs  
   - Cleans large intermediate files  

---

## Installation

Clone the repository:

git clone https://github.com/YOUR-USERNAME/modsim-batch-runner.git  
cd modsim-batch-runner  

Create virtual environment (recommended):

python -m venv .venv  
.venv\Scripts\activate  

Install dependencies:

pip install -r requirements.txt  

---

## Usage

Run a batch of scenarios:

python Run.py ^
  --csv_folder "path/to/DailyTimeseriesCSVFiles" ^
  --results_folder "path/to/output_folder" ^
  --base_folder "path/to/base_MODSIM_folder" ^
  --batchsize 8  

Run multiple scenario groups:

python BatchRunner.py  

---

## Input Requirements

Scenario CSV files:
- No header row  
- First two columns: year, month  
- Remaining columns: station data  

MODSIMNodes.xlsx must include:
- MODSIM node name  
- station index  
- multiplier  

---

## MODSIM Model Requirements

Base model folder structure:

<base_folder>/
├── MB_HydroSim.xy  
└── MB_HydroSim Custom Run/
    └── MB_HydroSim_CustomRun.exe  

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

- Do not upload proprietary or restricted files  

---

## Limitations

- Windows-based paths  
- Assumes fixed MODSIM structure  
- Uses fixed cleanup delay  
- Limited validation  

---

## Suggested Improvements

- Replace hard-coded paths  
- Add logging  
- Improve error handling  
- Add cross-platform support  
- Include sample dataset (if allowed)  
- Add unit tests  

---

## Applications

- Hydropower system stress testing  
- Climate change impact analysis  
- Scenario-based water resource modeling  
- Large-scale simulation automation  

---

## Citation

Gozini, H. (2026). MODSIM Batch Scenario Runner. GitHub repository.

---

## Author

Hamid Gozini

---

## License

This project is licensed under the MIT License.
