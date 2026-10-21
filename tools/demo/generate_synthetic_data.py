"""Generate the SYNTHETIC data files used by the demo archive.

Nothing produced here is a real measurement. The physics is only loosely
realistic (a copper cylinder with one off-axis tuning rod), so the demo
records, plots and CAD files look like the real thing.

Run from the repo root:  python tools/demo/generate_synthetic_data.py
"""

import csv
import hashlib
import struct
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parents[2]
VAULT = ROOT / "vault"
OFFREPO = ROOT / "tools" / "demo" / "_offrepo"  # stand-in for group storage; git-ignored
RNG = np.random.default_rng(20261022)

DEMO_STAMP = "SYNTHETIC DEMO DATA"

# --- toy cavity model --------------------------------------------------------
R_MM, L_MM = 25.4, 254.0
PIVOT_MM = ARM_MM = 6.5
G_GHZ = 0.014  # TM010 / intruder coupling


def rod_offset_mm(theta_deg):
    return PIVOT_MM * np.sqrt(2 + 2 * np.cos(np.radians(theta_deg)))


def f_tm010_bare(theta_deg):
    d = rod_offset_mm(theta_deg)
    return 4.95 + 0.95 * (1 - (d / 13.0) ** 2) ** 1.2


F_INTRUDER = float(f_tm010_bare(112.0))  # crossing placed at 112 deg


def f_intruder(theta_deg):
    return F_INTRUDER + 0.0004 * (theta_deg - 112.0)


def hybrid_modes(theta_deg):
    """Upper/lower hybrid frequencies and TM010 fraction of each."""
    f1, f2 = f_tm010_bare(theta_deg), f_intruder(theta_deg)
    mean, half = (f1 + f2) / 2, (f1 - f2) / 2
    split = np.sqrt(half**2 + G_GHZ**2)
    f_up, f_lo = mean + split, mean - split
    mix = 0.5 * (1 + half / split)  # TM010 weight in the upper branch
    return f_up, f_lo, mix, 1 - mix


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, header, rows, comments=()):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        for c in (f"# {DEMO_STAMP}",) + tuple(comments):
            fh.write(c + "\n")
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def stamp(fig):
    fig.text(0.99, 0.01, DEMO_STAMP, ha="right", va="bottom", fontsize=7, color="0.5")


# --- MEAS-2026-013: mode map -------------------------------------------------
def mode_map():
    rec = VAULT / "Measurements/2026/MEAS-2026-013 CAV-02 mode map"
    angles = np.arange(0, 181, 1.0)
    freqs = np.linspace(4.80, 6.10, 2601)
    s21 = np.full((angles.size, freqs.size), 1e-9)
    peaks = []
    for i, th in enumerate(angles):
        f_up, f_lo, w_up, w_lo = hybrid_modes(th)
        modes = [
            ("TM010-like" if w_up >= 0.5 else "TE-like", f_up, 1e-4 * (0.05 + w_up), 11000),
            ("TM010-like" if w_lo > 0.5 else "TE-like", f_lo, 1e-4 * (0.05 + w_lo), 11000),
            ("TM011-like", f_tm010_bare(th) + 0.42, 2e-5, 9000),
            ("TE-like", 5.93 - 0.0006 * th, 6e-6, 7000),
        ]
        for label, f0, amp, q in modes:
            q_obs = q * (1 + 0.03 * RNG.standard_normal())
            s21[i] += amp / (1 + (2 * q_obs * (freqs - f0) / f0) ** 2)
            if freqs[0] < f0 < freqs[-1]:
                peaks.append((th, label, round(f0 + 2e-5 * RNG.standard_normal(), 5),
                              int(q_obs), round(10 * np.log10(amp), 1)))
    s21_db = 10 * np.log10(s21) + 0.4 * RNG.standard_normal(s21.shape)

    write_csv(rec / "MEAS-2026-013_CAV-02_modemap_th000-180deg_peaks.csv",
              ["rod_angle_deg", "mode_label", "f_GHz", "Q_loaded", "S21_peak_dB"], peaks,
              ["# peak-finder v1.2 output; labels from field-pattern heuristics"])

    OFFREPO.mkdir(parents=True, exist_ok=True)
    raw = OFFREPO / "MEAS-2026-013_CAV-02_modemap_th000-180deg_raw.npz"
    np.savez_compressed(raw, angles_deg=angles, f_GHz=freqs, s21_dB=s21_db.astype(np.float32))

    fig, ax = plt.subplots(figsize=(8, 5), dpi=130)
    im = ax.pcolormesh(angles, freqs, s21_db.T, shading="auto", cmap="magma", vmin=-95, vmax=-35)
    ax.set_xlabel("Tuning-rod angle (deg)")
    ax.set_ylabel("Frequency (GHz)")
    ax.set_title("CAV-02 mode map — MEAS-2026-013 (295 K, air)")
    ax.annotate("avoided crossing\n(~112°)", xy=(112, F_INTRUDER), xytext=(135, 5.25),
                color="w", arrowprops=dict(color="w", arrowstyle="->"), fontsize=9)
    fig.colorbar(im, label="|S21| (dB)")
    stamp(fig)
    fig.tight_layout()
    fig.savefig(rec / "MEAS-2026-013_CAV-02_modemap_th000-180deg.png")
    plt.close(fig)
    return raw


# --- MEAS-2026-014/015: bead-pulls ------------------------------------------
def bead_pull(rec_name, rec_id, theta):
    rec = VAULT / f"Measurements/2026/{rec_name}"
    z = np.linspace(0, L_MM, 201)
    f_up, _, w_up, _ = hybrid_modes(theta)
    alpha = np.arccos(np.sqrt(w_up))
    e = np.cos(alpha) + np.sin(alpha) * np.sqrt(2) * np.cos(np.pi * z / L_MM)
    e2 = e**2 / np.max(e**2)
    df_khz = -42.0 * e2 * (1 + 0.01 * (z / L_MM - 0.5)) + 0.6 * RNG.standard_normal(z.size)
    tag = f"th{int(theta):03d}deg"
    write_csv(rec / f"{rec_id}_CAV-02_beadpull_{tag}_proc.csv",
              ["z_mm", "delta_f_kHz", "E_rel_sq"],
              [(round(a, 2), round(b, 3), round(max(-b / 42.0, 0), 4)) for a, b in zip(z, df_khz)],
              [f"# mode: TM010-like (upper branch), f0 = {f_up:.5f} GHz, rod angle = {theta} deg",
               "# E_rel_sq = -delta_f / 42 kHz (normalized to empty-cavity reference)"])

    raw = OFFREPO / f"{rec_id}_CAV-02_beadpull_{tag}_raw.csv"
    write_csv(raw, ["step", "z_mm", "f_res_GHz"],
              [(i, round(a, 2), round(f_up + b * 1e-6, 9)) for i, (a, b) in enumerate(zip(z, df_khz))])

    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=130)
    ax.plot(z, df_khz, ".", ms=3, color="C0")
    ax.set_xlabel("Bead position z (mm)")
    ax.set_ylabel("Δf (kHz)")
    ax.set_title(f"CAV-02 bead-pull, rod at {theta}° — {rec_id}")
    ax.set_ylim(-48, 3)
    ax.grid(alpha=0.3)
    stamp(fig)
    fig.tight_layout()
    fig.savefig(rec / f"{rec_id}_CAV-02_beadpull_{tag}.png")
    plt.close(fig)
    return raw


# --- SIM-2026-007: eigenmode sweep ------------------------------------------
def simulation():
    rec = VAULT / "Simulations/SIM-2026-007 CAV-02 eigenmode sweep"
    angles = np.arange(0, 181, 4.0)
    rows = []
    for th in angles:
        f_up, f_lo, w_up, w_lo = hybrid_modes(th)
        f_tm = f_up if w_up >= 0.5 else f_lo
        w = max(w_up, w_lo)
        c010 = 0.68 * w**2 - 0.0006 * abs(th - 90)
        offset = 0.0041 + 0.0009 * (th / 180 - 0.5) + 0.00015 * RNG.standard_normal()
        rows.append((th, round(f_tm - offset, 5), round(c010, 3)))
    write_csv(rec / "SIM-2026-007_CAV-02_eigenmode_th000-180deg_results.csv",
              ["rod_angle_deg", "f_TM010_GHz", "C010"], rows,
              ["# CST MWS 2025 eigenmode solver, tetrahedral mesh, PEC walls + surface impedance"])
    a, f, c = np.array(rows).T
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6), dpi=130)
    ax[0].plot(a, f, "o-", ms=3)
    ax[0].set(xlabel="Rod angle (deg)", ylabel="f TM010 (GHz)", title="Frequency")
    ax[1].plot(a, c, "o-", ms=3, color="C3")
    ax[1].set(xlabel="Rod angle (deg)", ylabel="C010", title="Form factor", ylim=(0, 0.8))
    for x in ax:
        x.grid(alpha=0.3)
    fig.suptitle("SIM-2026-007 — CAV-02 eigenmode sweep")
    stamp(fig)
    fig.tight_layout()
    fig.savefig(rec / "SIM-2026-007_CAV-02_eigenmode_th000-180deg.png")
    plt.close(fig)


# --- CAD: binary STL meshes + drawing ---------------------------------------
def _revolve(profile, n=96):
    """Triangles for a closed (r, z) profile revolved about the z axis."""
    t = np.linspace(0, 2 * np.pi, n + 1)
    tris = []
    for (r1, z1), (r2, z2) in zip(profile, profile[1:] + profile[:1]):
        for a, b in zip(t[:-1], t[1:]):
            p = lambda r, z, ang: (r * np.cos(ang), r * np.sin(ang), z)
            q1, q2, q3, q4 = p(r1, z1, a), p(r2, z2, a), p(r2, z2, b), p(r1, z1, b)
            tris += [(q1, q2, q3), (q1, q3, q4)]
    return tris


def _write_stl(path, tris, name):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as fh:
        fh.write(name.encode()[:80].ljust(80, b" "))
        fh.write(struct.pack("<I", len(tris)))
        for v1, v2, v3 in tris:
            nrm = np.cross(np.subtract(v2, v1), np.subtract(v3, v1))
            nrm = nrm / (np.linalg.norm(nrm) or 1)
            fh.write(struct.pack("<12fH", *nrm, *v1, *v2, *v3, 0))


def _barrel_profile(length, flange_t, flange_od=80.0, wall_od=60.0, bore=50.8):
    ri, ro, rf = bore / 2, wall_od / 2, flange_od / 2
    return [(ri, 0), (rf, 0), (rf, flange_t), (ro, flange_t), (ro, length - flange_t),
            (rf, length - flange_t), (rf, length), (ri, length)]


def cad():
    rec = VAULT / "CAD/CAD-CAV02-001 Cavity barrel"
    _write_stl(rec / "CAD-CAV02-001_barrel_revB.stl", _revolve(_barrel_profile(250.0, 8.0)),
               "CAD-CAV02-001 rev B SYNTHETIC DEMO")
    _write_stl(rec / "CAD-CAV02-001_barrel_revC.stl", _revolve(_barrel_profile(254.0, 12.0)),
               "CAD-CAV02-001 rev C SYNTHETIC DEMO")

    rod = VAULT / "CAD/CAD-CAV02-002 Tuning rod"
    prof = [(0.0, -10.0), (1.5, -10.0), (1.5, 0.0), (6.35, 0.0), (6.35, 252.0),
            (1.5, 252.0), (1.5, 262.0), (0.0, 262.0)]
    _write_stl(rod / "CAD-CAV02-002_tuning-rod_revA.stl", _revolve(prof, 64),
               "CAD-CAV02-002 rev A SYNTHETIC DEMO")

    with PdfPages(rec / "CAD-CAV02-001_barrel_revC_drawing.pdf") as pdf:
        fig, ax = plt.subplots(figsize=(11, 8.5))
        ax.set_aspect("equal")
        ax.axis("off")
        L, ft, rf, ro, ri = 254.0, 12.0, 40.0, 30.0, 25.4
        outline = [(0, rf), (ft, rf), (ft, ro), (L - ft, ro), (L - ft, rf), (L, rf)]
        for sgn in (1, -1):
            xs, ys = zip(*outline)
            ax.plot(xs, [sgn * y for y in ys], "k", lw=1.5)
            ax.plot([0, L], [sgn * ri, sgn * ri], "k--", lw=0.8)
            ax.fill_between([0, L], sgn * ri, sgn * ro, color="0.85", zorder=0)
        ax.plot([0, 0], [-rf, rf], "k", lw=1.5)
        ax.plot([L, L], [-rf, rf], "k", lw=1.5)
        ax.plot([-10, L + 10], [0, 0], "k-.", lw=0.6)

        def dim(x1, y1, x2, y2, text, off=(0, 0)):
            ax.annotate("", (x1, y1), (x2, y2), arrowprops=dict(arrowstyle="<->", lw=0.8))
            ax.text((x1 + x2) / 2 + off[0], (y1 + y2) / 2 + off[1], text, ha="center", fontsize=9)

        dim(0, -55, L, -55, "254.00 ±0.05", (0, -6))
        dim(L + 18, -ri, L + 18, ri, "Ø50.80 +0.02/-0", (16, 0))
        dim(-18, -rf, -18, rf, "Ø80.0", (-10, 0))
        dim(0, 50, ft, 50, "12.0", (0, 3))
        ax.text(L / 2, 2, "SECTION A-A", ha="center", fontsize=9)
        ax.set_xlim(-60, L + 70)
        ax.set_ylim(-130, 75)
        rows = [("PART", "CAD-CAV02-001  Cavity barrel"), ("REV", "C"),
                ("MATERIAL", "OFHC copper C10100, bore finish 0.4 µm Ra"),
                ("DRAWN", "M. Sekatchev  2026-09-30"), ("CHECKED", "Megan  2026-10-02"),
                ("NOTE", "DEMO DRAWING — NOT FOR FABRICATION")]
        for k, (a, b) in enumerate(rows):
            y = -78 - 8 * k
            ax.text(120, y, a, fontsize=8, weight="bold")
            ax.text(160, y, b, fontsize=8)
        ax.add_patch(plt.Rectangle((115, -125), 205, 54, fill=False, lw=1))
        pdf.savefig(fig)
        plt.close(fig)


# --- Analysis: sim vs measurement -------------------------------------------
def analysis():
    """Run the analysis script stored in the vault, exactly as a user would."""
    import runpy

    script = VAULT / "Analyses/ANA-2026-004 Sim vs measured tuning curve/ANA-2026-004_compare_sim_meas.py"
    runpy.run_path(str(script), run_name="__main__")


# --- Legacy: recovered 2019 plot ---------------------------------------------
def legacy():
    rec = VAULT / "Measurements/Legacy/LEGACY-2019-002 PBG-01 mode map (recovered)"
    x = np.linspace(0, 1, 60)
    rows = [(round(a, 3), round(6.9 + 0.8 * a + 0.01 * RNG.standard_normal(), 4),
             round(7.4 - 0.1 * a + 0.01 * RNG.standard_normal(), 4)) for a in x]
    write_csv(rec / "LEGACY-2019-002_PBG-01_modemap_unknown-conditions_recovered.csv",
              ["col1", "col2", "col3"], rows,
              ["# recovered from 'cavity_stuff/final_FINAL2.xlsx' (sheet 3); column meaning inferred"])
    fig, ax = plt.subplots(figsize=(6, 4), dpi=110)
    a, b, c = np.array(rows).T
    ax.plot(a, b, "x")
    ax.plot(a, c, "+")
    ax.set_title("final_FINAL2 (sheet 3)")
    stamp(fig)
    fig.savefig(rec / "LEGACY-2019-002_PBG-01_modemap_unknown-conditions_recovered.png")
    plt.close(fig)


# --- GALAXIS: count-rate comparison (internal) -------------------------------
def galaxis():
    rec = VAULT / "Measurements/2026/MEAS-2026-021 GALAXIS scintillator count rates"
    rows = []
    for config, mean in (("no-crystal", 25.0), ("CsI-coupled", 77.0)):
        for run in range(1, 6):
            rows.append((config, run, 300, round(mean * (1 + 0.04 * RNG.standard_normal()), 1)))
    write_csv(rec / "MEAS-2026-021_GXS-01_countrate_csi-vs-bare_proc.csv",
              ["configuration", "run", "live_time_s", "rate_cps"], rows)


# --- Meeting viewgraphs -------------------------------------------------------
def viewgraphs():
    rec = VAULT / "Meetings/2026/MTG-2026-10-08 Group meeting"
    mm = VAULT / "Measurements/2026/MEAS-2026-013 CAV-02 mode map/MEAS-2026-013_CAV-02_modemap_th000-180deg.png"
    bp = VAULT / "Measurements/2026/MEAS-2026-015 CAV-02 bead-pull at 112 deg/MEAS-2026-015_CAV-02_beadpull_th112deg.png"
    with PdfPages(rec / "MTG-2026-10-08_viewgraphs_cavity-update_MS.pdf") as pdf:
        fig = plt.figure(figsize=(11, 6.2))
        fig.text(0.5, 0.6, "CAV-02 tuning characterization", ha="center", fontsize=26)
        fig.text(0.5, 0.48, "Group meeting · 2026-10-08 · M. Sekatchev", ha="center", fontsize=14)
        stamp(fig)
        pdf.savefig(fig)
        plt.close(fig)
        for title, img in (("Mode map: avoided crossing at ~112°", mm),
                           ("Bead-pull at 112°: field strongly tilted", bp)):
            fig = plt.figure(figsize=(11, 6.2))
            fig.text(0.05, 0.92, title, fontsize=20)
            ax = fig.add_axes([0.1, 0.05, 0.8, 0.8])
            ax.imshow(plt.imread(img))
            ax.axis("off")
            pdf.savefig(fig)
            plt.close(fig)


if __name__ == "__main__":
    raws = [mode_map(),
            bead_pull("MEAS-2026-014 CAV-02 bead-pull at 60 deg", "MEAS-2026-014", 60),
            bead_pull("MEAS-2026-015 CAV-02 bead-pull at 112 deg", "MEAS-2026-015", 112)]
    simulation()
    cad()
    analysis()
    legacy()
    galaxis()
    viewgraphs()
    print(f"intruder/crossing frequency: {F_INTRUDER:.5f} GHz")
    for r in raws:
        print(f"raw  {r.name}  {r.stat().st_size} B  sha256:{sha256(r)}")
