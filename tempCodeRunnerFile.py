import streamlit as st
from handcalcs.decorator import handcalc
import math


def fy_bolt(f_ym:float, f_um:float):
    """
    Dowel or bolt yield strength
    f_ym = specified yield strength obtained from applicable material standards, MPa
    f_um = specified tensile strength obtained from applicable material standards, MPa
    """
    fy_bolt = (f_ym + f_um)/2
    return fy_bolt

def f_iP(G:float, d_F:float, Jx:float = 1.0) -> float:
    """
    Embedment strength for a fastener bearing parallel to grain (angle teta = 0°)
    """
    f_iP = 50*G*(1-0.01*d_F)*Jx
    return f_iP

def f_iQ(G:float, d_F:float) -> float:
    """
    Embedment strength for a fastener bearing perpendicular to grain (angle teta = 90°)
    """
    f_iQ = 22*G*(1-0.01*d_F)
    return f_iQ

@handcalc()
def f_iteta(teta:float, f_iP:float, f_iQ:float, K_D:float = 1.0, K_SF:float = 1.0, K_T:float = 1.0):
    """
    Embedment strength of member i for a fastener bearing at angle relative to the grain
    """
    f_iteta = f_iP * f_iQ /   ( f_iP * math.sin(math.radians(teta))**2   +   f_iQ * math.cos(math.radians(teta))**2 )   * K_D * K_SF * K_T
    return f_iteta

@handcalc()
def n_u(n_s:int, t_1:float, t_2:float, f_1:float, f_2:float,f_y:float, d_f:float )-> float:
    """
    Unit lateral yielding resistance
    n_s = number of shear planes = 2 or 3
    """
    n_ua = f_1 * d_f * t_1
    n_ub = f_2 * d_f * t_2 if n_s == 2 else 0
    n_uc =1/2 * f_2 * d_f * t_2 if n_s == 3 else 0
    n_ud = f_1 * d_f**2 *       (math.sqrt(1/6 * f_2 /(f_1 + f_2) * f_y / f_1) + 1/5 * t_1 / d_f)
    n_ue = f_1 * d_f**2 *       (math.sqrt(1/6 * f_2 /(f_1 + f_2) * f_y / f_1) + 1/5 * t_2 / d_f) if n_s == 2 else 0
    n_uf = f_1 * d_f**2 * 1/5 * (t_1 / d_f + f_2 / t_1 * t_2 / d_f) if n_s == 2 else 0
    n_ug = f_1 * d_f**2 *       (math.sqrt(2/3 * f_2 /(f_1 + f_2) * f_y / f_1))
    
    nu = min(n_ua, n_ub, n_ud, n_ue, n_uf, n_ug) if n_s == 2 else min(n_ua, n_uc, n_ud, n_ug)
    
    
    return nu, (n_ua, n_ub, n_uc, n_ud, n_ue, n_uf, n_ug)
    

# TESTS CODE RUNNER
n_s = 2
t_1 = 40
t_2 = 40
f_iP_value = 18.333
f_iQ_value = 8.067
f_y = 310
G=0.42
d_F=12.7
Jx=1.0
teta = 45

f_iP_value = f_iP(G, d_F, Jx)
f_iQ_value = f_iQ(G, d_F)
f_iteta_value = f_iteta(teta, f_iP_value, f_iQ_value)[1]
print(f"""
      f_iP = {f_iP_value}
      f_iQ = {f_iQ_value}
      f_iteta = {f_iteta_value}
      """)

# Résultat de la fonction n_u
results = n_u(n_s, t_1, t_2, f_iP_value, f_iQ_value, f_y, d_F)
print(results)

# Décompose le résultat brut
# n_u_latex = results[0]
# print(n_u_latex)
n_u_values = results[1]
print(n_u_values)
# n_u_values = results[1]
# print(n_u_values)

# n_ua, n_ub, n_uc, n_ud, n_ue, n_uf, n_ug = n_u_values[1]



# Affichage des valeurs extraites

# st.latex(f"n_u = {n_u_latex}*N")
# st.latex(f"n_{{u,a}}= {n_ua_latex}*N")
# st.latex(f"n_{{u,b}} = {n_ub_latex}*N")
# st.latex(f"n_{{u,c}} = {n_uc_latex}*N")
# st.latex(f"n_{{u,d}}= {n_ud_latex}*N")
# st.latex(f"n_{{u,e}} = {n_ue_latex}*N")
# st.latex(f"n_{{u,f}} = {n_uf_latex}*N")
# st.latex(f"n_{{u,g}}= {n_ug_latex}*N")

# st.write(f"Valeurs calculées :")
# st.write(f"n_u = {n_u_value}")
# st.write(f"n_ua = {n_ua}")
# st.write(f"n_ub = {n_ub}")
# st.write(f"n_uc = {n_uc}")
# st.write(f"n_ud = {n_ud}")
# st.write(f"n_ue = {n_ue}")
# st.write(f"n_uf = {n_uf}")
# st.write(f"n_ug = {n_ug}")





