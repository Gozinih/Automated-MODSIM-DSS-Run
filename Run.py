import os
import shutil
import argparse
from datetime import datetime
from multiprocessing import Pool
import psutil
import time

from ExtractData import extract_modsim_timeseries
from ModifyMODSIM import update_xy_timeseries
from RunMODSIM_Single import MODSIM_Run

# Constants
parser = argparse.ArgumentParser()
parser.add_argument("--csv_folder", required=True, help="Path to scenario CSV folder")
parser.add_argument("--results_folder", required=True, help="Path to MODSIM results folder")
parser.add_argument("--base_folder", required=True, help="Path to MODSIM model folder")
parser.add_argument("--batchsize", type=int, required=True, help="Number of Paralles Simulations")
args = parser.parse_args()
CSV_FOLDER = args.csv_folder
RESULTS_FOLDER = args.results_folder
BASE_FOLDER = args.base_folder
BATCH_SIZE = args.batchsize
EXE_RELATIVE_PATH = os.path.join("MB_HydroSim Custom Run", "MB_HydroSim_CustomRun.exe") #MB_HydroSim is the MODSIM model name, modify accordingly
XY_RELATIVE_PATH = "MB_HydroSim.xy"
files_to_remove = ["MB_HydroSim.xy", "MB_HydroSimOUTPUT.mdb"]

def run_scenario(csv_file):
    scenario_name = os.path.splitext(csv_file)[0]
    scenario_folder = os.path.join(RESULTS_FOLDER, f"{BASE_FOLDER}_{scenario_name}")

    # Prepare working directory
    if os.path.exists(scenario_folder):
        shutil.rmtree(scenario_folder)
    shutil.copytree(BASE_FOLDER, scenario_folder)

    # Extract and update .xy timeseries
    df = extract_modsim_timeseries(
        os.path.join(CSV_FOLDER, csv_file),
        "MODSIMNodes.xlsx",
        "1980-01-01"
    )
    xy_path = os.path.join(scenario_folder, XY_RELATIVE_PATH)
    update_xy_timeseries(xy_path, df, scenario_name)

    # Run MODSIM
    exe_path = os.path.join(scenario_folder, EXE_RELATIVE_PATH)
    MODSIM_Run(xy_path, exe_path, scenario_name)

    # Wait 2 minutes before cleaning up
    time.sleep(120)

    for filename in files_to_remove:
        file_path = os.path.join(scenario_folder, filename)
        if os.path.exists(file_path):
                os.remove(file_path)

def scenario_batches(scenarios, batch_size):
    for i in range(0, len(scenarios), batch_size):
        yield scenarios[i:i + batch_size]

if __name__ == "__main__":
    total_start = datetime.now()  # ⏱️ Start timer for the whole process

    csv_files = sorted([f for f in os.listdir(CSV_FOLDER) if f.endswith(".csv")])
    num_scenarios = len(csv_files)
    physical_cores = psutil.cpu_count(logical=False)
    batch_size = BATCH_SIZE

    #print(f"📊 Total {num_scenarios} scenarios, running in batches of {batch_size}...")

    scenario_groups = list(scenario_batches(csv_files, batch_size))

    for idx, batch in enumerate(scenario_groups, 1):
        #print(f"\n🚩 Starting batch {idx}/{len(scenario_groups)} with scenarios: {batch}")
        batch_start = datetime.now()
        with Pool(processes=len(batch)) as pool:
            pool.map(run_scenario, batch)
        batch_elapsed = datetime.now() - batch_start
        #print(f"✅ Finished batch {idx}/{len(scenario_groups)} in {batch_elapsed}")

    total_elapsed = datetime.now() - total_start
    #print(f"\n🎉 All scenarios completed in {total_elapsed} and remain in {RESULTS_FOLDER}.")
