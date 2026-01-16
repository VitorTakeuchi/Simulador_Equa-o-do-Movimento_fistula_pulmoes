import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Modelo Respiratório com Dois Pulmões", layout="wide")

st.title("Simulador Didático – Modelo Respiratório Distribuído")

st.markdown("### Equação do Movimento")
st.latex(r"P(t) = E\,V(t) + R\,\dot V(t) + \mathrm{PEEP}")

st.markdown(
"""
Agora o sistema é modelado como **dois pulmões em paralelo**:

- **Pulmão Direito:** normal  
- **Pulmão Esquerdo:** com fístula broncopulmonar  
- Ambos compartilham **a mesma pressão**
"""
)

dt = 0.01
t = np.arange(0, 20, dt)

st.sidebar.header("Parâmetros Globais")

PEEP = st.sidebar.slider("PEEP (cmH₂O)", 0.0, 15.0, 5.0, 0.5)
A = st.sidebar.slider("Amplitude do Volume Oscilatório (L)", 0.1, 1.0, 0.5, 0.05)
f = st.sidebar.slider("Frequência Respiratória (Hz)", 0.05, 0.6, 0.25, 0.01)

st.sidebar.header("Pulmão Direito (Normal)")
E_D = st.sidebar.slider("Elastância Direita (cmH₂O/L)", 5.0, 40.0, 20.0, 0.5)
R_D = st.sidebar.slider("Resistência Direita (cmH₂O·s/L)", 1.0, 20.0, 5.0, 0.5)
FRC_D = st.sidebar.slider("FRC Direita (L)", 0.8, 2.0, 1.2, 0.1)

st.sidebar.header("Pulmão Esquerdo (Com Fístula)")
E_E = st.sidebar.slider("Elastância Esquerda (cmH₂O/L)", 5.0, 40.0, 30.0, 0.5)
R_E = st.sidebar.slider("Resistência Esquerda (cmH₂O·s/L)", 1.0, 30.0, 10.0, 0.5)
FRC_E = st.sidebar.slider("FRC Esquerda (L)", 0.5, 2.0, 1.0, 0.1)

fistula_frac = st.sidebar.slider(
    "Fração de Volume Perdido pela Fístula", 0.0, 0.7, 0.3, 0.05
)

V_osc = A * np.sin(2 * np.pi * f * t)
dV_osc = np.gradient(V_osc, dt)

VD = FRC_D + V_osc
VE = FRC_E + (1 - fistula_frac) * V_osc

dVD = np.gradient(VD, dt)
dVE = np.gradient(VE, dt)

Pel_D = E_D * (VD - FRC_D)
Pel_E = E_E * (VE - FRC_E)

Pres_D = R_D * dVD
Pres_E = R_E * dVE

P_total = (Pel_D + Pel_E) / 2 + (Pres_D + Pres_E) / 2 + PEEP

V_total = VD + VE

st.subheader("Curvas Pressão × Volume")

fig, ax = plt.subplots(1, 3, figsize=(18, 5))

ax[0].plot(V_total, P_total)
ax[0].set_title("Curva Global")
ax[0].set_xlabel("Volume Total (L)")
ax[0].set_ylabel("Pressão (cmH₂O)")

ax[1].plot(VD, P_total)
ax[1].set_title("Pulmão Direito")
ax[1].set_xlabel("Volume Direito (L)")

ax[2].plot(VE, P_total)
ax[2].set_title("Pulmão Esquerdo com Fístula")
ax[2].set_xlabel("Volume Esquerdo (L)")

st.pyplot(fig)

