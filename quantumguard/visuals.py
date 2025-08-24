# visuals.py
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from .utils import bits_to_str

#push issue 
def plot_match_hist(match_array: np.ndarray):
    """Plot histogram of basis matches (True/False)."""
    fig, ax = plt.subplots()
    counts = [np.sum(match_array), len(match_array)-np.sum(match_array)]
    ax.bar(["Match", "Mismatch"], counts, color=["green","red"])
    ax.set_title("Basis Match Histogram")
    st.pyplot(fig)

def plot_qber_curve(qber_points: list[tuple[float,float]]):
    """Plot QBER vs Eve probability."""
    fig, ax = plt.subplots()
    if qber_points:
        x, y = zip(*qber_points)
        ax.plot(x, y, marker='o')
        ax.set_xlabel("Eve Interception Probability")
        ax.set_ylabel("QBER")
        ax.set_title("QBER Curve")
    st.pyplot(fig)

def plot_bloch_preview(alice_bases, alice_bits):
    """Show simplified Bloch-like representation."""
    fig, ax = plt.subplots(figsize=(10,1.5))
    x = np.arange(len(alice_bits))
    colors = ['blue' if b==0 else 'red' for b in alice_bits]
    markers = ['o' if basis==0 else '^' for basis in alice_bases]
    for xi, c, m in zip(x, colors, markers):
        ax.scatter(xi, 0.5, c=c, marker=m)
    ax.set_yticks([])
    ax.set_xlabel("Qubit index")
    ax.set_title("Alice's Bits & Bases Preview")
    st.pyplot(fig)
