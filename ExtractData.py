import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def extract_modsim_timeseries(csv_path, modsim_excel_path, start_date_str):
    """
    Extract MODSIM-compatible time series as a DataFrame.

    Parameters:
        csv_path (str): Path to the raw daily inflow CSV file (no header, first 2 cols = year, month)
        modsim_excel_path (str): Path to the MODSIM node mapping Excel file
        start_date_str (str): Start date in 'YYYY-MM-DD' format (e.g., '1980-01-01')

    Returns:
        pd.DataFrame: MODSIM-ready DataFrame with 'Date' and one column per MODSIM node (int values)
    """
    # Load MODSIM node mapping
    modsim_nodes = pd.read_excel(modsim_excel_path)

    # Load raw data (no header), skip first 2 columns
    raw_data = pd.read_csv(csv_path, header=None)
    station_data = raw_data.iloc[:, 2:]

    # Generate daily date strings
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    num_days = station_data.shape[0]
    dates = [(start_date + timedelta(days=i)).strftime("%m/%d/%Y 00:00:00") for i in range(num_days)]

    # Generate MODSIM columns
    modsim_series = {}
    for _, row in modsim_nodes.iterrows():
        modsim_name = row.iloc[0]
        station_index = int(row.iloc[1]) - 1  # Convert to 0-based
        multiplier = float(row.iloc[2])

        raw_values = station_data.iloc[:, station_index].values
        transformed = raw_values * multiplier * 86.4 * 100
        modsim_series[modsim_name] = transformed.astype(int)

    # Build final DataFrame
    columns = {"Date": pd.Series(dates, name="Date")}

    for name, series in modsim_series.items():
        columns[name] = pd.Series(series, name=name)

    df = pd.concat(columns.values(), axis=1).copy()

    return df
