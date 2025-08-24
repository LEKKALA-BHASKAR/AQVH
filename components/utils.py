import numpy as np
import json
from pathlib import Path
import streamlit as st  # <<--- ADD THIS

def bits_to_str(bits: np.ndarray) -> str:
    """Convert numpy bit array into string '010101'."""
    return "".join(str(int(b)) for b in bits)
#push issue 
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
    import pandas as pd
    df = pd.DataFrame({
        "Index": sim_result['final_key_idx_global'],
        "Alice": sim_result['final_key_bits'],
    })
    return df

def download_buttons(df, sim_result):
    """Streamlit buttons to download CSV / TXT keys."""
    csv_path = Path("exports") / "sim_result.csv"
    df.to_csv(csv_path, index=False)
    st.download_button("📥 Download CSV", str(csv_path), file_name="sim_result.csv")
    
    txt_path = save_key_to_file(sim_result['final_key_bits'], "final_key.txt")
    st.download_button("📥 Download Key (TXT)", str(txt_path), file_name="final_key.txt")
