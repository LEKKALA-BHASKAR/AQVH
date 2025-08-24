import streamlit as st
from .styles import inject
from .config import Defaults

inject()

#push issue 



NAV_ITEMS = ["Dashboard", "Simulator", "Theory", "Team", "FAQ", "Contact"]

def header():
    left, right = st.columns([1,1])
    with left:
        st.markdown("# 🔐 QuantumGuard: BB84 Quantum Key Distribution Simulator")
        st.markdown(
            "**Live, demo‑ready** BB84 with intercept‑resend Eve. Visualize basis sifting, estimate QBER, and export the sifted key.")
    with right:
        st.markdown("<div style='text-align:right' class='small'>Made with <b>Streamlit</b> + <b>NumPy</b> + <b>Qiskit (optional visuals)</b></div>", unsafe_allow_html=True)


def sidebar_nav():
    with st.sidebar:
        st.markdown("## Navigation")
        page = st.radio("Go to", NAV_ITEMS, index=1)
        st.markdown("---")
        st.markdown("### Simulation Parameters")
        n_bits = st.slider("Qubits (N)", 16, 4096, Defaults.n_bits, step=16)
        eve_on = st.checkbox("Enable Eve", value=True)
        eve_prob = st.slider("Eve interception prob", 0.0, 1.0, Defaults.eve_probability, step=0.05, disabled=not eve_on)
        sample_fraction = st.slider("Sample fraction (of sifted)", 0.05, 0.5, Defaults.sample_fraction, step=0.05)
        qber_threshold = st.slider("QBER accept threshold", 0.01, 0.25, Defaults.qber_threshold, step=0.01)
        seed = st.number_input("Random seed (0 = random)", value=0, min_value=0, step=1)
        seed_val = None if seed == 0 else int(seed)

        c1, c2 = st.columns(2)
        with c1:
            run = st.button("▶️ Run Simulation", use_container_width=True)
        with c2:
            sweep = st.button("📈 Parameter Sweep", use_container_width=True)

        params = dict(
            n_bits=int(n_bits),
            eve_probability=float(eve_prob if eve_on else 0.0),
            sample_fraction=float(sample_fraction),
            qber_threshold=float(qber_threshold),
            seed=seed_val,
        )
        cmds = {"run": run, "sweep": sweep}
    return page, params, cmds


def section_theory():
    st.markdown("## 📚 Theory: BB84 in a Nutshell")
    st.markdown(
        "- **Preparation (Alice)**: encodes random bits in random bases **Z** (|0⟩,|1⟩) or **X** (|+⟩,|−⟩).\n"
        "- **Measurement (Bob)**: chooses random bases. Matches yield correlated bits (the **sifted key**).\n"
        "- **Eavesdropper (Eve)**: intercept‑resend forces a basis; wrong guesses inject errors.\n"
        "- **QBER**: fraction of disagreements in a revealed sample; if above threshold → **abort**.\n"
        "- **Security**: measurement of non‑orthogonal states leaves a statistical footprint.")


def section_team():
    st.markdown("## 👥 Team")
    st.write("— Alice: Preparation & Encoding\n\n— Bob: Measurement & Verification\n\n— Eve: Adversarial Testing\n\n— You: Demo Pilot 😄")
def section_contact():
    import streamlit as st
    st.markdown("## ✉️ Contact")
    st.write(
        "For queries, please reach out to **QuantumGuard Team** at:\n\n"
        "- Email: support@quantumguard.io\n"
        "- GitHub: [QuantumGuard](https://github.com/your-repo)\n"
        "- Or use the form below (demo only)."
    )
    st.text_input("Your Name")
    st.text_input("Your Email")
    st.text_area("Message")
    st.button("Send Message")


def section_faq():
    st.markdown("## ❓ FAQ")
    st.write("**Why does QBER rise with Eve?** Wrong‑basis interceptions randomize outcomes after sifting.\n\n"
             "**Do we use real hardware?** This demo simulates BB84 info‑flow; physics intuition is preserved.\n\n"
             "**Can I export the key?** Yes — CSV report and TXT key downloads are built‑in.")

    st.markdown("<span class='small'>© 2025 QuantumGuard • Built for hackathons and live classes.</span>", unsafe_allow_html=True)

def footer():
    st.markdown(
"<hr/><p style='text-align:center; font-size: 13px;'>© 2025 QuantumGuard • Made with  Streamlit</p>",
        unsafe_allow_html=True
    )
