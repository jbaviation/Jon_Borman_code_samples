''''spectra_equiv.py takes in Spectra Sensor measurements and calculates equivalent
relative humidity and dew point.'''

import CoolProp.CoolProp as cp
import CoolProp.HumidAirProp as hap
import pandas as pd

# Conversion constants
FT2M = 3.208        # Distance ft to m
K2R = 1.8           # Temperature K to degR
KPA2PSI = 0.145038  # Pressure kPa to psi
KGM2LBFT = 0.062428 # Density kg/m^3 to lbm/ft^3

# Standard constants
MAIR = cp.PropsSI('M','T',300,'P',101325,'air')*1e3  # Molar mass of dry air (g/mol)
MH2O = cp.PropsSI('M','T',300,'P',10.1,'water')*1e3  # Molar mass of water (g/mol)


# Vapor pressure calculation (checked and PASSED)
#  inputs: mmr     mass mixing ratio
#          p_psi   pressure in area of sample (psi)
#  output: p_w     vapor pressure (psi)
def vapor_pressure(mmr, p_psi):
    try:
        p_w = p_psi * mmr / (MH2O / MAIR + mmr)
    except:
        p_w = 0.0
    return p_w

# Humidity ratio (aka mass mixing ratio)
#  inputs: t       temperature in area of sample (K)
#          t_d     dew point temperature in area of sample (K)
#          p       pressure in area of sample (Pa)
#  output: mmr     mass mixing ratio
def humidity_ratio(t, t_d, p):
    # CoolProp
    try:
        mmr = hap.HAPropsSI('W','T',t,'D',t_d,'P',p)
    except:
        mmr = 0.9415
    return mmr

# Humidity ratio (aka mass mixing ratio)
#  inputs: ppmv    parts per million by volume water vapor
#  output: mmr     mass mixing ratio
def humidity_ratio2(ppmv):
    z = ppmv * 1e-6   # mole ratio from ppmv
    return z * (MH2O/MAIR)

# Mole ratio (actually ppmv)
#  inputs: mmr      mass mixing ratio
#  output: ppmv     parts per million by volume water vapor 
def mole_ratio(mmr):
    return (MAIR*mmr/MH2O) * 1e6

# Dew Point calculation (checked and PASSED)
#  inputs: mmr     mass mixing ratio
#          p_psi   pressure in area of sample (psi)
#  output: t_d     dew point temperature (F)
def dew_point(mmr, p_psi):
    # Vapor pressure
    p_w_psi = vapor_pressure(mmr, p_psi)

    # Convert to SI units
    p_w = p_w_psi / (KPA2PSI/1000)
    p = p_psi / (KPA2PSI/1000)

    # # ASHRAE method
    # t_d = 90.12 + 26.412 * np.log(p_w) + 0.8927 * np.log(p_w)**2

    # CoolProp method
    try:
        t_d = hap.HAPropsSI('D','W',mmr,'P',p,'T',300)
    except:
        t_d = 0.0

    return (t_d-273.15)*9/5 + 32  # converted to degreesF


# Relative humidity calculation (checked and PASSED)
#  inputs: t_f     temperature in area of sample (degF)
#          mmr     mass mixing ratio
#          p_psi   pressure in area of sample (psi)
#  output: rh      relative humidity (0-1)
def relative_humidity1(t_f, mmr, p_psi):
    # Convert to SI units
    t = (t_f-32)*5/9 + 273.15   # Kelvin
    p = p_psi / (KPA2PSI/1000)  # Pascals

    # Calculate dew point (K)
    t_d = (dew_point(mmr,p_psi)-32)*5/9 + 273.15

    # CoolProp
    try:
        rh = hap.HAPropsSI('R','T',t,'D',t_d,'P',p)
    except:
        if t<t_d:   # HAPropsSI doesn't work with supersaturated air; set to 1.0
            rh = 1.0
        elif t<=0.0 or t_d<=0.0:   # low humidity; return 0.0 
            rh = 0.0
        else:   # unknown error; return error value
            rh = -1.0

    return rh

# Relative humidity calculation
#  inputs: t       temperature in area of sample (K)
#          t_d     dew point temperature in area of sample (K)
#          p       pressure in area of sample (Pa)
#  output: rh      relative humidity (0-1)
def relative_humidity2(t, t_d, p):
    # CoolProp
    try:
        rh = hap.HAPropsSI('R','T',t,'D',t_d,'P',p)
    except:
        if t<t_d:   # HAPropsSI doesn't work with supersaturated air; set to 1.0
            rh = 1.0
        elif t<=0.0 or t_d<=0.0:   # low humidity; return 0.0 
            rh = 0.0
        else:   # unknown error; return error value
            rh = -1.0

    return rh

# Calculate ratio of specific heats
#  inputs:  t     temperature (degF)
#           p     pressure (psi)
#           mmr   mass mixing ratio (kgDA/kgWV)
#  output:  gam   mixture ratio of specific heats
def gamma(t,p,mmr):
    t_K = (t-32)*5/9 + 273.15     # Kelvin
    p_Pa = p / (KPA2PSI/1000)     # Pascals

    p_w = p_Pa * mmr / (MH2O/MAIR + mmr)  # vapor pressure (Pa)
    p_a = p_Pa - p_w   # partial pressure of air (Pa)

    CP = 'CPMASS'
    CV = 'CVMASS'

    try:
        gam_air = cp.PropsSI(CP,'T',t_K,'P',p_a,'air')/cp.PropsSI(CV,'T',t_K,'P',p_a,'air')
        gam_h2o = cp.PropsSI(CP,'T',t_K,'P',p_w,'water')/cp.PropsSI(CV,'T',t_K,'P',p_w,'water')

        w_h2o = mmr/(1+mmr)   # specific humidity (mass fraction water vapor)
        w_air = 1 - w_h2o     # mass fraction of dry air

        gam_mix = gam_air*w_air + gam_h2o*w_h2o   # gamma of mixture
    except:
        gam_mix = 0.0

    return gam_mix


# Calculate humid air density
#  inputs:  t     temperature (degF)
#           p     pressure (psi)
#           mmr   mass mixing ratio (kgDA/kgWV)
#  output:  rho   mixture density (lbm/ft3)
def density(t,p,mmr):
    t_K = (t-32)*5/9 + 273.15     # Kelvin
    p_Pa = p / (KPA2PSI/1000)     # Pascals

    p_w = p_Pa * mmr / (MH2O/MAIR + mmr)  # vapor pressure (Pa)
    p_a = p_Pa - p_w   # partial pressure of air (Pa)

    try:
        rho_air = cp.PropsSI('D','T',t_K,'P',p_a,'air')    # density kg/m3
        rho_h2o = cp.PropsSI('D','T',t_K,'P',p_w,'water')  # density kg/m3
        rho_mix = (rho_air + rho_h2o) * KGM2LBFT           # density lbm/ft3
    except:
        rho_mix = 0.0

    return rho_mix
#
# # Air density calculation
# #  inputs: t       temperature in area of sample (K)
# #          t_d     dew point temperature in area of sample (K)
# #          rh      relative humidity (0-1) (enter -1 if not known)
# #          p       pressure in area of sample (Pa)
# # NOTE: either t_d or rh must be known
# #  output: rho     humid air density (kg/m^3)
# def air_density(t, t_d, rh, p):
#
#     rh_pct = np.where(rh<0, relative_humidity(t,t_d,p), rh)  # numpy version of the code below
#     # if rh < 0.0:
#     #     rh_pct = relative_humidity(t, t_d, p)
#     # else:
#     #     rh_pct = rh
#
#     pvs = cp.PropsSI('P', 'T', t, 'Q', 1, 'water')    # Saturation vapor pressure
#     pv = rh_pct * pvs                                 # Vapor pressure (or partial pressure of water)
#     pa = p - pv                                       # Partial pressure of dry air
#
#     rhoa = cp.PropsSI('D','T',t,'P',pa,'air')     # Partial density of dry air
#     rhoh = cp.PropsSI('D','T',t,'P',pvs,'water')  # Partial density of water vapor
#
#     return rhoa + rhoh
