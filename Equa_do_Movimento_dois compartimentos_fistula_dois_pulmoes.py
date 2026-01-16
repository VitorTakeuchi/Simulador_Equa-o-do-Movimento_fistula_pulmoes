import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Simulador Respiratório – Comparação de Modelos",
    layout="wide"
)

st.title("Simulador Didático do Sistema Respiratório")

st.markdown("### Modelo 1 – Compartimento Pulmonar Único")
st.latex(r"P(t) = E\,V(t) + R\,\dot V(t) + \mathrm{PEEP}")

st.markdown("### Modelo 2 – Pulmão Direito e Esquerdo (Dois Compartimentos)")
st.latex(r"\dot V_D = \frac{P(t) - E_D V_D}{R_D}")
st.latex(r"\dot V_E = \frac{P(t) - E_E V_E}{R_E}")

dt = 0.01
t = np.arange(0, 20, dt)

st.sidebar.header("Entrada Ventilatória")

A = st.sidebar.slider("Amplitude do Volume [L]", 0.1, 1.0, 0.5, 0.05)
f = st.sidebar.slider("Frequência Respiratória [Hz]", 0.05, 0.6, 0.25, 0.01)
PEEP = st.sidebar.slider("PEEP [cmH₂O]", 0.0, 15.0, 5.0, 0.5)

V_in = A * np.sin(2 * np.pi * f * t)
dV_in = np.gradient(V_in, dt)

st.sidebar.header("Modelo 1 – Compartimento Único")

E = st.sidebar.slider("Elastância E [cmH₂O/L]", 5.0, 50.0, 20.0, 0.5)
R = st.sidebar.slider("Resistência R [cmH₂O·s/L]", 0.0, 30.0, 5.0, 0.5)

P_single = E * V_in + R * dV_in + PEEP

st.sidebar.header("Modelo 2 - Pulmões Separados")

ED = st.sidebar.slider("Elastância Pulmão Direito", 5.0, 50.0, 25.0, 0.5)
RD = st.sidebar.slider("Resistência Pulmão Direito", 1.0, 30.0, 6.0, 0.5)

EE = st.sidebar.slider("Elastância Pulmão Esquerdo", 5.0, 50.0, 15.0, 0.5)
RE = st.sidebar.slider("Resistência Pulmão Esquerdo", 1.0, 30.0, 4.0, 0.5)

fistula = st.sidebar.checkbox("Ativar fístula no pulmão direito")

Rf = st.sidebar.slider(
    "Resistência da fístula (direita)",
    5.0, 200.0, 50.0, 5.0,
    disabled=not fistula
)

VD = np.zeros_like(t)
VE = np.zeros_like(t)

P_drive = P_single 

for i in range(1, len(t)):

    dVD = (P_drive[i] - ED * VD[i-1]) / RD

    if fistula:
        dVD -= P_drive[i] / Rf

    VD[i] = VD[i-1] + dVD * dt

    dVE = (P_drive[i] - EE * VE[i-1]) / RE
    VE[i] = VE[i-1] + dVE * dt

V_total_2 = VD + VE

col1, col2 = st.columns(2)

with col1:
    st.subheader("Modelo 1 – Compartimento Único")

    fig1, ax1 = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

    ax1[0].plot(t, V_in)
    ax1[0].set_ylabel("Volume (L)")
    ax1[0].set_title("Volume de Entrada")

    ax1[1].plot(t, P_single)
    ax1[1].set_ylabel("Pressão (cmH₂O)")
    ax1[1].set_xlabel("Tempo (s)")

    st.pyplot(fig1)

with col2:
    st.subheader("Modelo 2 – Pulmões Separados")

    fig2, ax2 = plt.subplots(3, 1, figsize=(6, 8), sharex=True)

    ax2[0].plot(t, VD, label="Pulmão Direito")
    ax2[0].plot(t, VE, label="Pulmão Esquerdo")
    ax2[0].set_ylabel("Volume (L)")
    ax2[0].legend()

    ax2[1].plot(t, V_total_2)
    ax2[1].set_ylabel("Volume Total (L)")

    ax2[2].plot(t, P_drive)
    ax2[2].set_ylabel("Pressão (cmH₂O)")
    ax2[2].set_xlabel("Tempo (s)")

    st.pyplot(fig2)

st.subheader("Curvas Pressão × Volume")

fig3, ax3 = plt.subplots(figsize=(7, 4))

ax3.plot(V_in, P_single, label="Modelo Único")
ax3.plot(V_total_2, P_drive, label="Dois Pulmões")

ax3.set_xlabel("Volume (L)")
ax3.set_ylabel("Pressão (cmH₂O)")
ax3.legend()

st.pyplot(fig3)