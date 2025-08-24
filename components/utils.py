import numpy as np
import json
from pathlib import Path
import streamlit as st
import pandas as pd  # Added pandas import

def bits_to_str(bits: np.ndarray) -> str:
    """Convert numpy bit array into string '010101'."""
    return "".join(str(int(b)) for b in bits)

def bits_to_hex(bits: np.ndarray) -> str:
    """Convert bit array into hex string."""
    bit_str = bits_to_str(bits)
    if len(bit_str) % 4 != 0:
        bit_str = bit_str.ljust(len(bit_str) + (4 - len(bit_str) % 4), "0")
    return hex(int(bit_str, 2))[2:].upper()

def save_key_to_file(bits: np.ndarray, filename: str, out_dir: str = "exports") -> Path:
    """Save final key to TXT file."""
    Path(out_dir).mkdir(exist_ok=True)
    filepath = Path(out_dir) / filename
    with open(filepath, "w") as f:
        f.write(bits_to_str(bits))
    return filepath

def save_log_to_json(sim_result: dict, filename: str, out_dir: str = "exports") -> Path:
    """Save the full simulation result as JSON."""
    Path(out_dir).mkdir(exist_ok=True)
    filepath = Path(out_dir) / filename
    with open(filepath, "w") as f:
        json.dump(sim_result, f, indent=2, default=str)
    return filepath

def build_run_dataframe(sim_result: dict):
    """Convert simulation result to pandas DataFrame for display."""
    df = pd.DataFrame({
        "Index": sim_result['final_key_idx_global'],
        "Alice": sim_result['final_key_bits'],
    })
    return df

def download_buttons(df, sim_result):
    """Streamlit buttons to download CSV / TXT keys."""
    # Ensure exports directory exists before saving any files
    Path("exports").mkdir(exist_ok=True)
    
    csv_path = Path("exports") / "sim_result.csv"
    df.to_csv(csv_path, index=False)
    
    # Read the CSV file content for download
    with open(csv_path, "r") as f:
        csv_data = f.read()
    
    st.download_button(
        "📥 Download CSV",
        data=csv_data,
        file_name="sim_result.csv",
        mime="text/csv"
    )
    
    # Save and create download buttons for other formats
    txt_path = save_key_to_file(sim_result['final_key_bits'], "final_key.txt")
    with open(txt_path, "r") as f:
        txt_data = f.read()
    st.download_button(
        "📥 Download Key (TXT)",
        data=txt_data,
        file_name="final_key.txt",
        mime="text/plain"
    )
    
    json_path = save_log_to_json(sim_result, "sim_result.json")
    with open(json_path, "r") as f:
        json_data = f.read()
    st.download_button(
        "📥 Download Log (JSON)",
        data=json_data,
        file_name="sim_result.json",
        mime="application/json"
    )