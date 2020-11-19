''' TC.py allows the user to convert voltage to a temperature with various TC types.
'''

def TC_typeJ(V=0.0,TdegF=32.0,VtoT=True):
    ''' Initialize type J TC curves.  Function goes both ways but defaults to VtoT (or Voltage to Temperature).
        Sourced from: https://www.keysight.com/upload/cmc_upload/All/5306OSKR-MXD-5501-040106_2.htm?&cc=US&lc=eng'''
    if VtoT:
        mV = 2.0*V+4.0  # Convert voltage over a resistor
        print(mV)
        if mV <= 0.0:
            # Coefficients for temperature range -210 C to 0 C and Voltage range -8.095 mV to 0.0 mV:
            c0 = 0.0
            c1 = 1.9528268 * 10**1
            c2 = -1.2286185
            c3 = -1.0752178
            c4 = -5.9086933 * 10**-1
            c5 = -1.7256713 * 10**-1
            c6 = -2.8131513 * 10**-2
            c7 = -2.3963370 * 10**-3
            c8 = -8.3823321 * 10**-5
        elif mV > 0.0:
            # Coefficients for temperature range 0 C to 760 C and Voltage range 0.0 mV to 42.919 mV:
            c0 = 0.0
            c1 = 1.978425 * 10**1
            c2 = -2.001204 * 10**-1
            c3 = 1.036969 * 10**-2
            c4 = -2.549687 * 10**-4
            c5 = 3.585153 * 10**-6
            c6 = -5.344285 * 10**-8
            c7 = 5.099890 * 10**-10
            c8 = 0.0
        else:
            pass

        TdegC = c0+c1*mV+c2*mV**2+c3*mV**3+c4*mV**4+c5*mV**5+c6*mV**6+c7*mV**7+c8*mV**8
        return TdegC*1.8 + 32   # return TdegF
    else:
        # The coefficients for temperature range -210 C to 760 C are:
        c0 = 0.0
        c1 = 5.0381187815 * 10**-2
        c2 = 3.0475836930 * 10**-5
        c3 = -8.5681065720 * 10**-8
        c4 = 1.3228195295 * 10**-10
        c5 = -1.7052958337 * 10**-13
        c6 = 2.0948090697 * 10**-16
        c7 = -1.2538395336 * 10**-19
        c8 = 1.5631725697 * 10**-23

        TdegC = (TdegF-32)/1.8
        mV = c0+c1*TdegC+c2*TdegC**2+c3*TdegC**3+c4*TdegC**4+c5*TdegC**5+c6*TdegC**6+c7*TdegC**7+c8*TdegC**8
        return mV/1000  # return Voltage

def TC_typeT(V=0.0,TdegF=32.0,VtoT=True):
    mV = V*0.1818 - 99.8182/1000  # Convert voltage over a resistor
    TdegC = (mV*1000)/43.0
    return TdegC*1.8 + 32

