from handcalcs.decorator import handcalc

@handcalc()
def calc_Mr(b:float, d:float, phi:float, f_y:float):
    """
    Calculate Mr of a rectangular section
    """
    S_x = (b*d**2) /6 # Elastic section modulus
    M_r = phi * f_y * S_x # Moment resistance
    return M_r