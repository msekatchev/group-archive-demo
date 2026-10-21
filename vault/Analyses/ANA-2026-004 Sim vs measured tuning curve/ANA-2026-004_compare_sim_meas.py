"""ANA-2026-004: compare simulated (SIM-2026-007) and measured (MEAS-2026-013) TM010 tuning.

Reads only files that live in the archive, so anyone with the vault can rerun it:
    python "vault/Analyses/ANA-2026-004 Sim vs measured tuning curve/ANA-2026-004_compare_sim_meas.py"
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[1]
SIM = VAULT / "Simulations/SIM-2026-007 CAV-02 eigenmode sweep/SIM-2026-007_CAV-02_eigenmode_th000-180deg_results.csv"
MEAS = VAULT / "Measurements/2026/MEAS-2026-013 CAV-02 mode map/MEAS-2026-013_CAV-02_modemap_th000-180deg_peaks.csv"


def read_csv(path, **kw):
    """Archive CSVs carry '#' provenance lines above the header row."""
    lines = [ln for ln in path.read_text().splitlines() if not ln.startswith("#")]
    return np.genfromtxt(lines, delimiter=",", names=True, encoding="utf-8", **kw)


sim = read_csv(SIM)
meas = read_csv(MEAS, dtype=None)
tm = meas[meas["mode_label"] == "TM010-like"]

f_meas_at_sim = np.interp(sim["rod_angle_deg"], tm["rod_angle_deg"], tm["f_GHz"])
resid_mhz = 1e3 * (f_meas_at_sim - sim["f_TM010_GHz"])
offset = np.median(resid_mhz)

fig, ax = plt.subplots(2, 1, figsize=(7, 5.5), dpi=130, sharex=True,
                       gridspec_kw={"height_ratios": [2, 1]})
ax[0].plot(tm["rod_angle_deg"], tm["f_GHz"], ".", ms=3, label="measured (MEAS-2026-013)")
ax[0].plot(sim["rod_angle_deg"], sim["f_TM010_GHz"], "-", label="simulated (SIM-2026-007)")
ax[0].set_ylabel("f TM010 (GHz)")
ax[0].legend()
ax[1].plot(sim["rod_angle_deg"], resid_mhz, "o", ms=3, color="C3")
ax[1].axhline(offset, color="0.4", ls="--", lw=0.8)
ax[1].set_xlabel("Rod angle (deg)")
ax[1].set_ylabel("meas − sim (MHz)")
ax[1].text(5, offset + 0.6, f"median offset {offset:+.1f} MHz", fontsize=8)
for a in ax:
    a.grid(alpha=0.3)
fig.suptitle("ANA-2026-004 — CAV-02 tuning: simulation vs measurement")
fig.text(0.99, 0.01, "SYNTHETIC DEMO DATA", ha="right", va="bottom", fontsize=7, color="0.5")
fig.tight_layout()
fig.savefig(HERE / "ANA-2026-004_CAV-02_tuning_sim-vs-meas.png")
print(f"median offset meas - sim = {offset:+.2f} MHz")
