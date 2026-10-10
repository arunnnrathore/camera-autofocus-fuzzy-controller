
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Camera Autofocus Fuzzy Controller", layout="wide")


# ----------------------------- Fuzzy core -----------------------------------
def trimf(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    if x == b:
        return 1.0
    return (x - a) / (b - a) if x < b else (c - x) / (c - b)


def trapmf(x, a, b, c, d):
    if x <= a or x >= d:
        return 0.0
    if b <= x <= c:
        return 1.0
    return (x - a) / (b - a) if x < b else (d - x) / (d - c)


E_MFS = {
    'NL': lambda x: trapmf(x, -10, -10, -8, -4),
    'NS': lambda x: trimf(x, -8, -4, 0),
    'Z':  lambda x: trimf(x, -4, 0, 4),
    'PS': lambda x: trimf(x, 0, 4, 8),
    'PL': lambda x: trapmf(x, 4, 8, 10, 10),
}
dE_MFS = {
    'N': lambda x: trapmf(x, -5, -5, -3, 0),
    'Z': lambda x: trimf(x, -3, 0, 3),
    'P': lambda x: trapmf(x, 0, 3, 5, 5),
}
O_MFS = {
    'NL': lambda x: trapmf(x, -50, -50, -40, -20),
    'NS': lambda x: trimf(x, -40, -20, 0),
    'Z':  lambda x: trimf(x, -20, 0, 20),
    'PS': lambda x: trimf(x, 0, 20, 40),
    'PL': lambda x: trapmf(x, 20, 40, 50, 50),
}
O_PEAK = {'NL': -45.0, 'NS': -20.0, 'Z': 0.0, 'PS': 20.0, 'PL': 45.0}

RULES = [
    ('R1', 'NL', 'N', 'NL'), ('R2', 'NL', 'Z', 'NL'),
    ('R3', 'NS', 'N', 'NS'), ('R4', 'NS', 'Z', 'NS'),
    ('R5', 'Z',  'Z', 'Z'),
    ('R6', 'PS', 'Z', 'PS'), ('R7', 'PS', 'P', 'PL'),
    ('R8', 'PL', 'P', 'PL'),
]


def infer(E, dE):
    muE = {k: f(E) for k, f in E_MFS.items()}
    mudE = {k: f(dE) for k, f in dE_MFS.items()}
    fired = []
    for rid, e_set, de_set, o_set in RULES:
        w = min(muE[e_set], mudE[de_set])
        if w > 0:
            fired.append((rid, e_set, de_set, w, o_set))
    if not fired:
        return 0.0, fired
    num = sum(w * O_PEAK[o_set] for _, _, _, w, o_set in fired)
    den = sum(w for _, _, _, w, o_set in fired)
    return num / den, fired


def plot_mfs(universe, mfs, marker, title, xlabel):
    x = np.linspace(universe[0], universe[1], 400)
    fig, ax = plt.subplots(figsize=(5, 3))
    for name, f in mfs.items():
        ax.plot(x, [f(v) for v in x], label=name, linewidth=2)
    ax.axvline(marker, color='black', linestyle='--', linewidth=1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Membership')
    ax.legend(fontsize=8)
    ax.set_ylim(-0.05, 1.05)
    fig.tight_layout()
    return fig


# ------------------------------- UI ------------------------------------
st.title("Camera Autofocus - Fuzzy Logic Controller")
st.caption(
    "Two-input, single-output Mamdani FLC - Sharpness Error (E) and its "
    "Rate of Change (dE) drive the Lens Motor Step (O)."
)

with st.sidebar:
    st.header("Inputs")
    E = st.slider("Sharpness Error, E", -10.0, 10.0, 4.0, 0.1)
    dE = st.slider("Rate of Change of Error, dE", -5.0, 5.0, 2.0, 0.1)
    st.markdown("---")
    st.write("Based on the PBL report's Tables 4-7 (membership functions "
             "and 8-rule rule base).")

crisp, fired = infer(E, dE)

col1, col2, col3 = st.columns(3)
col1.metric("Sharpness Error (E)", f"{E:.2f}")
col2.metric("Rate of Change (dE)", f"{dE:.2f}")
direction = "Forward" if crisp > 0 else ("Backward" if crisp < 0 else "Hold")
col3.metric("Lens Motor Step (O*)", f"{crisp:.2f}", direction)

st.markdown("### Fired Rules")
if fired:
    df = pd.DataFrame(
        [{"Rule": rid, "E-set": e_set, "dE-set": de_set,
          "Firing Strength": round(w, 3), "Output Set": o_set}
         for rid, e_set, de_set, w, o_set in fired]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.warning("No rule fired for this input combination (rule-base gap) - "
               "controller defaults to O* = 0.")

st.markdown("### Membership Function Fuzzification")
c1, c2, c3 = st.columns(3)
with c1:
    st.pyplot(plot_mfs((-10, 10), E_MFS, E, "Sharpness Error (E)", "E"))
with c2:
    st.pyplot(plot_mfs((-5, 5), dE_MFS, dE, "Rate of Change (dE)", "dE"))
with c3:
    st.pyplot(plot_mfs((-50, 50), O_MFS, crisp, "Lens Motor Step (O)", "O"))

st.markdown("### Control Surface")
if st.checkbox("Show full O = f(E, dE) surface (may take a second)"):
    E_range = np.linspace(-10, 10, 50)
    dE_range = np.linspace(-5, 5, 50)
    Eg, dEg = np.meshgrid(E_range, dE_range)
    Og = np.zeros_like(Eg)
    for i in range(Eg.shape[0]):
        for j in range(Eg.shape[1]):
            Og[i, j], _ = infer(Eg[i, j], dEg[i, j])
    fig, ax = plt.subplots(figsize=(6, 4))
    cs = ax.contourf(Eg, dEg, Og, levels=20, cmap="coolwarm")
    ax.plot(E, dE, "k*", markersize=15)
    fig.colorbar(cs, label="O*")
    ax.set_xlabel("E")
    ax.set_ylabel("dE")
    st.pyplot(fig)
