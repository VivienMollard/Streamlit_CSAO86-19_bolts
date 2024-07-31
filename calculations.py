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


def n_u(n_s:int, t_1:float, t_2:float, f_1:float, f_2:float,f_y:float, d_f:float )-> float:
    """
    Unit lateral yielding resistance
    n_s = number of shear planes = 2 or 3
    """
    # mode a
    nu_a = f_1 * d_f * t_1
    
    # mode b
    if n_s == 2:
        nu_b = f_2 * d_f * t_2
    elif n_s == 3:
        nu_b = 0
        
    # mode c
    if n_s == 2:
        nu_c = 0
    elif n_s == 3:
        nu_c = 1/2 * f_2 * d_f * t_2
        
    # mode d   
    nu_d = f_1 * d_f**2 * ( math.sqrt( 1/6 * f_2 /(f_1 + f_2) * f_y / f_1) + 1/5 * t_1 / d_f  )
    
    # mode e
    if n_s == 2:
        nu_e = f_1 * d_f**2 * ( math.sqrt( 1/6 * f_2 /(f_1 + f_2) * f_y / f_1) + 1/5 * t_2 / d_f  )
    elif n_s == 3:
        nu_e = 0
        
    # mode f
    if n_s == 2:
        nu_f = f_1 * d_f**2 * 1/5 * ( t_1 / d_f +  f_2 / t_1 * t_2 / d_f )
    elif n_s == 3:
        nu_f = 0
        
    # mode g
    nu_g = f_1 * d_f**2 * ( math.sqrt( 2/3 * f_2 /(f_1 + f_2) * f_y / f_1))
    
    # MINIMUM VALUE
    if n_s == 2:
        nu = min(nu_a, nu_b, nu_d, nu_e, nu_f, nu_g)
    elif n_s == 3:
        nu = min(nu_a, nu_c, nu_d, nu_g)
    
    
    return nu, (nu_a, nu_b, nu_c, nu_d, nu_e, nu_f, nu_g)
    

# TESTS CODE RUNNER
G=0.42
d=12.7
Jx=1.0
teta = 45

f_iP_value = f_iP(G, d, Jx)
f_iQ_value = f_iQ(G, d)
f_iteta_value = f_iteta(teta, f_iP_value, f_iQ_value)[1]
print(f"""
      f_iP = {f_iP_value}
      f_iQ = {f_iQ_value}
      f_iteta = {f_iteta_value}
      """)


nu_value = n_u(2, 40, 40, 18.333, 8.067, 310, 12.7)[0]
nu_a, nu_b, nu_c, nu_d, nu_e, nu_f, nu_g = n_u(2, 40, 40, 18.333, 8.067, 310, 12.7)[1]

print(f"nu_a = {nu_a}")
print(f"nu_b = {nu_b}")
print(f"nu_c = {nu_c}")
print(f"nu_d = {nu_d}")
print(f"nu_e = {nu_e}")
print(f"nu_f = {nu_f}")
print(f"nu_g = {nu_g}")

print(f"n_u = {nu_value}")
