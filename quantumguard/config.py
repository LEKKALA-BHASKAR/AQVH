from dataclasses import dataclass
from typing import Optional

@dataclass
class Defaults:
    n_bits: int = 256
    eve_probability: float = 0.5
    sample_fraction: float = 0.2
    qber_threshold: float = 0.11
    seed: Optional[int] = None

#push issue 




