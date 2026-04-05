import os
import shutil
import subprocess
from time import perf_counter
from tqdm import tqdm

# MB_HydroSim is the MODSIM model name

# Files you want to keep from each run
files_to_keep = {
    "MB_HydroSimHydroTargetOutput.csv",
    "MB_HydroSimRES_STOROutput.csv"
}

TOTAL_RUNS = 20 # 20 Folders (EG1 to EG20), each has 25 scenairos
batchsize = 13  # number of parallel run for scenarios

overall_start = perf_counter()
with tqdm(total=TOTAL_RUNS, desc="MODSIM batches", unit="run") as pbar:
    for i in range(1, TOTAL_RUNS + 1):
        iter_start = perf_counter()

        suffix = f"EG{i}"
        csv_folder = f"C:/Users/gozinih/Desktop/EG/Scenarios/Scenarios_{suffix}/DailyTimeseriesCSVFiles" # Patch to .csv file in each scenario to read inflow and demand
        results_folder = f"C:/Users/gozinih/Desktop/EG/MODSIM/MODSIM_{suffix}" # Patch to generate the MODSIM model
        finalresults_folder = f"C:/Users/gozinih/Desktop/EG/Results/Results_{suffix}" # Patch to save the requaired results from each MODSIM run
        base_folder = "MB_HydroSim_Folder" # MODSIM model folder, having .xy file and .exe file

        # --- Run MODSIM batch ---
        subprocess.run([
            "python", "Run.py",
            "--csv_folder", csv_folder,
            "--results_folder", results_folder,
            "--base_folder", base_folder,
            "--batchsize", str(batchsize)
        ], check=True)

        # --- Copy selected result files ---
        os.makedirs(finalresults_folder, exist_ok=True)
        for scenario in os.listdir(results_folder):
            src_folder = os.path.join(results_folder, scenario)
            dst_folder = os.path.join(finalresults_folder, scenario)

            if not os.path.isdir(src_folder):
                continue  # Skip if not a folder

            os.makedirs(dst_folder, exist_ok=True)

            for fname in files_to_keep:
                src_file = os.path.join(src_folder, fname)
                dst_file = os.path.join(dst_folder, fname)

                if os.path.isfile(src_file):
                    shutil.copy2(src_file, dst_file)
                else:
                    tqdm.write(f"⚠️ Missing in {scenario}: {fname}")

        # --- Remove heavy MODSIM results folder ---
        try:
            shutil.rmtree(results_folder)
        except Exception as e:
            tqdm.write(f"❌ Error removing {results_folder}: {e}")

        # --- Update progress bar ---
        iter_elapsed = perf_counter() - iter_start
        pbar.set_postfix_str(f"{suffix}: {iter_elapsed:.1f}s")
        pbar.update(1)

overall_elapsed = perf_counter() - overall_start
print(f"⏱️ Finished {TOTAL_RUNS} runs in {overall_elapsed/60:.1f} min ({overall_elapsed:.1f} s).")
