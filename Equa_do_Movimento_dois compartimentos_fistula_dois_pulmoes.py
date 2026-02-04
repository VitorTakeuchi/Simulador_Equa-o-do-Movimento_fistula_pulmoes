import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Simulador Respiratório – Modelos Comparativos",
    layout="wide"
)

st.title("Simulador do Sistema Respiratório")

st.markdown("### Modelo 1 – Compartimento Pulmonar Único")
st.latex(r"P(t) = E\,V(t) + R\,\dot V(t) + \mathrm{PEEP}")

st.markdown("### Modelo 2 – Dois Pulmões (Direito / Esquerdo)")
st.latex(r"\dot V_i = \frac{P(t) - E_i (V_i - FRC_i)}{R_i}")

# =============================
# TEMPO
# =============================
dt = 0.01
t = np.arange(0, 20, dt)

# =============================
# ENTRADA VENTILATÓRIA
# =============================
st.sidebar.header("Entrada Ventilatória")

A = st.sidebar.slider("Amplitude do Volume (L)", 0.1, 1.0, 0.5, 0.05)
f = st.sidebar.slider("Frequência Respiratória (Hz)", 0.05, 0.6, 0.25, 0.01)
PEEP = st.sidebar.slider("PEEP (cmH₂O)", 0.0, 15.0, 5.0, 0.5)

V_in = A * np.sin(2 * np.pi * f * t)
dV_in = np.gradient(V_in, dt)

st.sidebar.header("Modelo Pulmonar Único")

E = st.sidebar.slider("Elastância E", 5.0, 50.0, 20.0, 0.5)
R = st.sidebar.slider("Resistência R", 0.0, 30.0, 5.0, 0.5)

P_single = E * V_in + R * dV_in + PEEP

st.sidebar.header("Pulmão Direito")

ED = st.sidebar.slider("Elastância Direita", 5.0, 50.0, 25.0, 0.5)
RD = st.sidebar.slider("Resistência Direita", 1.0, 30.0, 6.0, 0.5)
FRC_D = st.sidebar.slider("FRC Direita (L)", 0.8, 2.0, 1.2, 0.1)

st.sidebar.header("Pulmão Esquerdo")

EE = st.sidebar.slider("Elastância Esquerda", 5.0, 50.0, 15.0, 0.5)
RE = st.sidebar.slider("Resistência Esquerda", 1.0, 30.0, 4.0, 0.5)
FRC_E = st.sidebar.slider("FRC Esquerda (L)", 0.8, 2.0, 1.0, 0.1)

st.sidebar.header("Fístulas (Vazamento de Volume)")

fistula_D = st.sidebar.slider(
    "Fração de vazamento – Pulmão Direito",
    0.0, 0.6, 0.0, 0.05
)

fistula_E = st.sidebar.slider(
    "Fração de vazamento – Pulmão Esquerdo",
    0.0, 0.6, 0.3, 0.05
)

VD = np.zeros_like(t)
VE = np.zeros_like(t)

VD[0] = FRC_D
VE[0] = FRC_E

P_drive = P_single

for i in range(1, len(t)):

    # Pulmão Direito
    dVD = (P_drive[i] - ED * (VD[i-1] - FRC_D)) / RD
    dVD *= (1 - fistula_D)   # fístula direita ON/OFF
    VD[i] = VD[i-1] + dVD * dt

    # Pulmão Esquerdo
    dVE = (P_drive[i] - EE * (VE[i-1] - FRC_E)) / RE
    dVE *= (1 - fistula_E)   # fístula esquerda ON/OFF
    VE[i] = VE[i-1] + dVE * dt

V_total = VD + VE

col1, col2 = st.columns(2)

with col1:
    st.subheader("Modelo Pulmonar Único")

    fig1, ax1 = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

    ax1[0].plot(t, V_in)
    ax1[0].set_ylabel("Volume (L)")
    ax1[0].set_title("Entrada de Volume")

    ax1[1].plot(t, P_single)
    ax1[1].set_ylabel("Pressão (cmH₂O)")
    ax1[1].set_xlabel("Tempo (s)")

    st.pyplot(fig1)

with col2:
    st.subheader("Modelo Distribuído (Dois Pulmões)")

    fig2, ax2 = plt.subplots(3, 1, figsize=(6, 8), sharex=True)

    ax2[0].plot(t, VD, label="Pulmão Direito")
    ax2[0].plot(t, VE, label="Pulmão Esquerdo")
    ax2[0].legend()
    ax2[0].set_ylabel("Volume (L)")

    ax2[1].plot(t, V_total)
    ax2[1].set_ylabel("Volume Total (L)")

    ax2[2].plot(t, P_drive)
    ax2[2].set_ylabel("Pressão (cmH₂O)")
    ax2[2].set_xlabel("Tempo (s)")

    st.pyplot(fig2)

st.subheader("Curvas Pressão × Volume")

fig3, ax3 = plt.subplots(figsize=(8, 5))

ax3.plot(V_in, P_single, label="Modelo Único")
ax3.plot(V_total, P_drive, label="Global (enganosa)", linewidth=2)
ax3.plot(VD, P_drive, "--", label="Pulmão Direito")
ax3.plot(VE, P_drive, "--", label="Pulmão Esquerdo")

ax3.set_xlabel("Volume (L)")
ax3.set_ylabel("Pressão (cmH₂O)")
ax3.legend()

st.pyplot(fig3)
