import os
import subprocess
from datetime import datetime

def MODSIM_Run(xy_file_path, exe_file_path, scenario_name):
    """
    Runs MODSIM for a scenario and reports execution time and result.
    """
    exe_dir = os.path.dirname(os.path.abspath(exe_file_path))
    xy_path = os.path.abspath(xy_file_path)
    exe_path = os.path.abspath(exe_file_path)
    start_time = datetime.now()
    #print(f"🚀 Running MODSIM for scenario: {scenario_name}")

    try:
        result = subprocess.run(
            [exe_path, xy_path],
            cwd=exe_dir,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False
        )
        elapsed = datetime.now() - start_time
        #print(f"✅ Scenario {scenario_name} completed in {elapsed}.")

    except subprocess.CalledProcessError as e:
        elapsed = datetime.now() - start_time
        print(f"❌ Scenario {scenario_name} failed after {elapsed}: {e}")
        print(f"Error:\n{e.stderr}\n")