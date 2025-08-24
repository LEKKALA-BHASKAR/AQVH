# simulator.py
import numpy as np
import random
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import streamlit as st

_rng = np.random.default_rng()

BASIS_LABELS = {0: "Z", 1: "X"}
#push issue 



def simulate_bb84(
    n_bits: int,
    eve_probability: float,
    sample_fraction: float,
    qber_threshold: float,
    seed: Optional[int] = None
) -> Dict:
    """
    Simulate BB84 with intercept-resend Eve.

    Returns a dictionary with the full run data:
      - alice_bits, alice_bases, bob_bases, bob_results
      - eve_acted, eve_bases
      - sift_idx, sifted_alice, sifted_bob
      - sample_positions, qber, final_key_bits, decision, timestamp
    """
    # Seed handling for reproducibility
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # 1) Alice: random bits and bases
    alice_bits = _rng.integers(0, 2, size=n_bits)
    alice_bases = _rng.integers(0, 2, size=n_bits)  # 0: Z, 1: X

    # 2) Bob: random measurement bases
    bob_bases = _rng.integers(0, 2, size=n_bits)

    # Eve: acts on each qubit with probability eve_probability
    eve_acted = _rng.random(n_bits) < eve_probability
    eve_bases = _rng.integers(0, 2, size=n_bits)

    bob_results = np.zeros(n_bits, dtype=int)

    # Process each qubit
    for i in range(n_bits):
        a_bit = int(alice_bits[i])
        a_basis = int(alice_bases[i])
        b_basis = int(bob_bases[i])

        if not eve_acted[i]:
            # No Eve: Bob gets perfect result when basis matches else random
            bob_results[i] = a_bit if b_basis == a_basis else int(_rng.integers(0, 2))
        else:
            # Eve intercepts: measures in her basis, resends her outcome
            e_basis = int(eve_bases[i])
            e_bit = a_bit if e_basis == a_basis else int(_rng.integers(0, 2))
            # Bob measures the state prepared by Eve
            bob_results[i] = e_bit if b_basis == e_basis else int(_rng.integers(0, 2))

    # 3) Basis sifting: keep indices where Alice and Bob bases matched
    matches = (alice_bases == bob_bases)
    sift_idx = np.where(matches)[0]
    sifted_alice = alice_bits[sift_idx]
    sifted_bob = bob_results[sift_idx]

    # 4) Error check: choose a sample subset to estimate QBER
    n_sift = len(sift_idx)
    if n_sift == 0:
        # No sifted bits => QBER undefined; set to 0 and empty key
        sample_positions_local = np.array([], dtype=int)
        qber = 0.0
        final_key_bits = np.array([], dtype=int)
        final_key_idx_global = np.array([], dtype=int)
    else:
        sample_size = max(1, int(np.floor(sample_fraction * n_sift))) if sample_fraction > 0 else 0
        if sample_size > 0:
            # sample positions are indices into the sifted arrays (0..n_sift-1)
            sample_positions_local = _rng.choice(n_sift, size=sample_size, replace=False)
            sample_errors = np.sum(sifted_alice[sample_positions_local] != sifted_bob[sample_positions_local])
            qber = float(sample_errors) / float(sample_size)
            # remove revealed sample from final key
            mask = np.ones(n_sift, dtype=bool)
            mask[sample_positions_local] = False
            final_key_bits = sifted_alice[mask]
            final_key_idx_global = sift_idx[mask]
        else:
            # No sampling requested => estimate QBER over entire sift (useful for debug)
            sample_positions_local = np.array([], dtype=int)
            # avoid division by zero
            if n_sift > 0:
                qber = float(np.sum(sifted_alice != sifted_bob)) / float(n_sift)
            else:
                qber = 0.0
            final_key_bits = sifted_alice
            final_key_idx_global = sift_idx

    # Decision based on threshold
    decision = "Secure (Accept Key)" if qber <= qber_threshold else "Eavesdropping Detected (Abort)"

    return {
        'alice_bits': alice_bits,
        'alice_bases': alice_bases,
        'bob_bases': bob_bases,
        'bob_results': bob_results,
        'eve_acted': eve_acted,
        'eve_bases': eve_bases,
        'sift_idx': sift_idx,
        'sifted_alice': sifted_alice,
        'sifted_bob': sifted_bob,
        'sample_positions': sample_positions_local,
        'qber': float(qber),
        'final_key_bits': final_key_bits,
        'final_key_idx_global': final_key_idx_global,
        'decision': decision,
        'timestamp': datetime.now().isoformat(),
    }


def run_simulation(params: Dict, cmds: Dict) -> Dict:
    """
    Wrapper to be used from Streamlit:
      - params: dict with keys n_bits, eve_probability, sample_fraction, qber_threshold, seed
      - cmds: dict with keys 'run', 'sweep' (booleans from buttons)
    Persists the latest result in st.session_state['last_run'].
    """
    if cmds.get('run') or 'last_run' not in st.session_state:
        res = simulate_bb84(
            n_bits=int(params.get('n_bits', 256)),
            eve_probability=float(params.get('eve_probability', 0.0)),
            sample_fraction=float(params.get('sample_fraction', 0.2)),
            qber_threshold=float(params.get('qber_threshold', 0.11)),
            seed=params.get('seed', None)
        )
        st.session_state['last_run'] = res
        return res
    return st.session_state.get('last_run', {})


def sweep_eve(params: Dict) -> List[Tuple[float, float]]:
    """
    Sweep several Eve interception probabilities and return list of (p, qber).
    Uses coarse set [0.0, 0.25, 0.5, 0.75, 1.0] by default.
    """
    pts = []
    for p in [0.0, 0.25, 0.5, 0.75, 1.0]:
        tmp = simulate_bb84(
            n_bits=int(params.get('n_bits', 256)),
            eve_probability=float(p),
            sample_fraction=float(params.get('sample_fraction', 0.2)),
            qber_threshold=float(params.get('qber_threshold', 0.11)),
            seed=params.get('seed', None)
        )
        pts.append((p, tmp['qber']))
    return pts


if __name__ == "__main__":
    # Quick local test: run a simulation and print a short summary
    test_params = {
        'n_bits': 128,
        'eve_probability': 0.5,
        'sample_fraction': 0.2,
        'qber_threshold': 0.11,
        'seed': 42
    }
    result = simulate_bb84(**test_params)
    print("Sifted bits:", len(result['sift_idx']))
    print("QBER (sampled):", result['qber'])
    print("Decision:", result['decision'])
    print("Final key length:", len(result['final_key_bits']))
