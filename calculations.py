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


@handcalc(override='long')
def n_u(n_s:int, t_1:float, t_2:float, f_1:float, f_2:float,f_y:float, d_f:float )-> float:
    """
    Unit lateral yielding resistance
    n_sp = number of shear planes = 1 or 2
    """
    n_ua = f_1 * d_f * t_1
    n_ub = f_2 * d_f * t_2 if n_s == 1 else 0
    n_uc =1/2 * f_2 * d_f * t_2 if n_s == 2 else 0
    n_ud = f_1 * d_f**2 *       (math.sqrt(1/6 * f_2 /(f_1 + f_2) * f_y / f_1) + 1/5 * t_1 / d_f)
    n_ue = f_1 * d_f**2 *       (math.sqrt(1/6 * f_2 /(f_1 + f_2) * f_y / f_1) + 1/5 * t_2 / d_f) if n_s == 1 else 0
    n_uf = f_1 * d_f**2 * 1/5 * (t_1 / d_f + f_2 / t_1 * t_2 / d_f) if n_s == 1 else 0
    n_ug = f_1 * d_f**2 *       (math.sqrt(2/3 * f_2 /(f_1 + f_2) * f_y / f_1))
    
    n_u = min(n_ua, n_ub, n_ud, n_ue, n_uf, n_ug) if n_s == 1 else min(n_ua, n_uc, n_ud, n_ug)
    
    
    return n_u, (n_ua, n_ub, n_uc, n_ud, n_ue, n_uf, n_ug)


@handcalc()
def N_r(n_u:float, n_s:float, n_F:int, phi_y:float = 0.8 )-> float:
    """
    yielding resistance
    """
    N_r = phi_y * n_u * n_s * n_F
    
    return N_r


def calculate_Nr_for_diameters(n_s: int, n_F: int, t_1: float, t_2: float, f_y: float, teta_1: float, teta_2: float, g_1: float, g_2: float, phi_y: float = 0.8, K_D: float = 1.0, K_SF: float = 1.0, K_T: float = 1.0) -> list:
    diameters = [12.7, 15.9, 19.1, 22.2, 25.4]
    #diameters = [9.52, 12.7, 15.9, 19.1, 22.2, 25.4, 28.6, 31.8, 34.9, 38.1]
    Nr_for_diameters = []
    
    for d_F in diameters:
        # Calculer les valeurs de f_iP et f_iQ pour g_1
        f_1P= f_iP(g_1, d_F)
        f_1Q = f_iQ(g_1, d_F)
        f_1teta = f_iteta(teta_1, f_1P, f_1Q, K_D, K_SF, K_T)[1]
        f_1 = f_1teta

        # Calculer les valeurs de f_iP et f_iQ pour g_2
        f_2P = f_iP(g_2, d_F)
        f_2Q = f_iQ(g_2, d_F)
        f_2teta = f_iteta(teta_2, f_2P, f_2Q , K_D, K_SF, K_T)[1]
        f_2 = f_2teta

        # Calculer n_u et N_r
        n_u_value = n_u(n_s, t_1, t_2, f_1, f_2, f_y, d_F)[1][0]
        N_r_value = N_r(n_u_value, n_s, n_F, phi_y)[1]
        Nr_for_diameters.append(N_r_value)
    
    return diameters, Nr_for_diameters 



# TESTS CODE RUNNER
# n_s = 2
# n_F = 4
# t_1 = 40
# t_2 = 40
# f_iP_value = 18.333
# f_iQ_value = 8.067
# f_y = 310
# G=0.42
# d_F=12.7
# Jx=1.0
# teta = 45
# phi_y = 0.8

# f_iP_value = f_iP(G, d_F, Jx)
# f_iQ_value = f_iQ(G, d_F)
# f_iteta_value = f_iteta(teta, f_iP_value, f_iQ_value)[1]
# print(f"""
#       f_iP = {f_iP_value}
#       f_iQ = {f_iQ_value}
#       f_iteta = {f_iteta_value}
#       """)

# results = n_u(n_s, t_1, t_2, f_iP_value, f_iQ_value, f_y, d_F)
# n_u_latex = results[0]
# n_u_value = results[1][0]
# n_u_allValues = results[1][1]
# n_ua, n_ub, n_uc, n_ud, n_ue, n_uf, n_ug = n_u_allValues
# phi_y = 0.8
# N_r_value = N_r(n_u_value, n_s, n_F, phi_y)

# print(f'nu = {n_u_value}')   
# print(f'Nr = {N_r_value}') 


# Exemple d'appel de la fonction
n_s = 1
n_F = 4
t_1 = 40
t_2 = 40
f_y = 310
teta_1 = 0
teta_2 = 90
g_1 = 0.42
g_2 = 0.42

Nr_for_diameters = calculate_Nr_for_diameters(n_s, n_F, t_1, t_2, f_y, teta_1, teta_2, g_1, g_2)[1]
print(Nr_for_diameters)
