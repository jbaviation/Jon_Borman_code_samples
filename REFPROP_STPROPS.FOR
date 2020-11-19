C------------------------------------------------------------------------------
C  REFPROP_STPROPS.FOR
C    REFPROP wrapper function for station properties including velocity, Mach
C    number, static temperature and pressure, density, enthalpy, entropy,
C    heat capacities, and speed of sounds.
C
C  Modifications:
C  2018-11-11 - Added ability to omit the area and airflow if static pressure
C                or temperature is known. (J. Borman)
C  2018-06-05 - Added option to include static temperature and pressure
C                measurements. (J. Borman)
C  2018-05-07 - Initial version called from CUSTOMER_CALCS.TAG (J. Borman)
C
C  Call REFPROP_STPROPS(TT_DEGR,TS_DEGR,PT_PSI,PS_PSI,XH2O,A_IN2,WF_PPS,
C                         RHO_GS,GAM_GS,C_GS,
C                  TSTOT,PSTOT,WH2OTOT,VTOT,MTOT,CTOT,RHOTOT,GAMTOT,HTOT)
C
C  Inputs:
C    TT_DEGR  - Measured total air temperature (degR)
C    TS_DEGR  - Measured static air temp (degR) (INPUT '-1.0' IF UNKNOWN)
C    PT_PSI   - Measured total air pressure (psia)
C    PS_PSI   - Measured static air press (psia) (INPUT '-1.0' IF UNKNOWN)
C    XH2O     - Mole fraction of water vapor (dimless)
C    A_IN2    - Fan inlet area (in^2)   (INPUT '-1.0' IF UNKNOWN)
C    WF_PPS   - Airflow at fan (lbm/s)  (INPUT '-1.0' IF UNKNOWN)
C    RHO_GS   - Density initial guess (lbm/ft^3)
C    GAM_GS   - Ratio of specific heats initial guess (dimless)
C    C_GS     - Speed of sound initial guess (ft/s)
C NOTE: RHO_GS, GAM_GS, C_GS are not important if TS_DEGR and PS_PSI are known
C
C  Outputs:
C    TSTOT    - Static temperature at fan (degR)
C    PSTOT    - Static pressure at fan (psia)
C    WH2OTOT  - Mass fraction of water vapor (dimless)
C    VTOT     - Flow velocity at fan (ft/s)
C    MTOT     - Flow Mach number at fan (dimless)
C    CTOT     - Speed of sound at fan (ft/s)
C    RHOTOT   - Combined air density at fan (lbm/ft^3)
C    GAMTOT   - Combined ratio of specific heats at fan (dimless)
C    HTOT     - Combined enthalpy at fan (BTU/lbm-R)
C------------------------------------------------------------------------------

      SUBROUTINE REFPROP_STPROPS(
     *             TT_DEGR,TS_DEGR,PT_PSI,PS_PSI,XH2O,A_IN2,WF_PPS,
     *             RHO_GS,GAM_GS,C_GS,
     *             TSTOT,PSTOT,WH2OTOT,VTOT,MTOT,CTOT,
     *             RHOTOT,GAMTOT,HTOT)

C------------------------------------------------------------------------------
C  Data Recording Parameters
C------------------------------------------------------------------------------
      COMMON/QAREC/DONT_USE_RDGN,BAROM,IRDTY,IRECB,IABO,IREC,IESP(2),
     *            IERLOG,IRCS,IDONT_USE,ISTORCYC,ICYCTY,ICYC,ICCS,
     *            IBATCH,NETACT,IAPREC,IAPCLR,IAPRCS,IPRCS,IAPSCAN,
     *            NAVGSCAN,ISTDAVG,ITRANSFL,NOREC_CAL,ISGHEAD(5),
     *            IDATAVIS,IVIDEOREC,LRNT,IREADNO_MASS,
     *            IDRTRANS,ICOMFILE,IREADNO_DUMPS,ISSA
      INTEGER*2 IRDTY,IRECB,IABO,IREC,IESP,IERLOG,IRCS,IDONT_USE,
     *          ISTORCYC,ICYCTY,ICYC,ICCS,IBATCH,NETACT,IAPREC,
     *          IAPCLR,IAPRCS,IPRCS,IAPSCAN,NAVGSCAN,ISTDAVG,
     *          ITRANSFL,NOREC_CAL,ISGHEAD,IDATAVIS,IVIDEOREC,LRNT,
     *          IDRTRANS,ICOMFILE

C------------------------------------------------------------------------------
C  Include Standard Constants
C------------------------------------------------------------------------------
      INCLUDE 'CONSTANTS.FOR'

C------------------------------------------------------------------------------
C  LOCAL VARIABLE DECLARATIONS
C------------------------------------------------------------------------------

C  Local Variables
      INTEGER ICOUNT
      REAL EGAM
      REAL A2,V2,M2,TS2,PS2,PAP2,PHP2
      REAL RHOA2,GAMA2,HA2,RHOH2,GAMH2,HH2,RHO2,GAM2,H2,C2
      REAL WAIR,WH2O,MMIX,RMIX
      REAL CTOT,HTOT,GAMTOT,RHOTOT,TSTOT,PSTOT,MTOT,VTOT,WH2OTOT


C  REFPROP inputs/outputs
      REAL*8 PPROP,TPROP,PPROPH,PPROPA,RHOPROP,RHOPA,RHOPH
      REAL*8 WMM,TTRP,TNBPT,TC,PC,DC,ZC,ACF,DIP,RGASRP
      REAL*8 RHO,E,H,S,CV,CP,W,HJT,RHOL,RHOV,XLIQ,XVAP,P
      PARAMETER (NCMAX=20)   ! max number of components in mixture
      CHARACTER HRF*3, HERR*255
      CHARACTER*255 HF(NCMAX), HFMIX
      REAL*8 X(2)

C Air Composition (molar fractions)
      X(1) = 0.5000d0
      X(2) = 0.5000d0

C------------------------------------------------------------------------------
C  REFPROP Initialization
C------------------------------------------------------------------------------

C NOT NECESSARY TO CALL SETUP FROM THIS SUBROUTINE

C------------------------------------------------------------------------------
C  REFPROP Calculations
C------------------------------------------------------------------------------

C Fan Inlet Area (in^2)
      A2 = A_IN2

C Iterative Calculation of Fan Inlet Gamma
C Initial Values
      RHO2 = RHO_GS
      GAM2 = GAM_GS
      C2 = C_GS
      EGAM = 1.0
      ICOUNT = 0

      DO WHILE (EGAM .GT. 0.0001)
        ICOUNT = ICOUNT + 1

        IF ((A2 .GT. 0.0) .AND. (WF_PPS .GE. 0.0)) THEN  !Calculate Velocity
C         Velocity at the fan face
          V2 = WF_PPS / ( RHO2 * (A2 / 144.0) )

C         Mach number at the fan face
          M2 = V2 / C2

        ELSE IF (PS_PSI .GT. 0.0) THEN
C         Mach number from isentropic relation
          M2 = SQRT(2.0/(GAM2-1.0)*((PT_PSI/PS_PSI)
     *          **((GAM2-1.0)/GAM2)-1.0))
          V2 = M2 * C2

        ELSE IF (TS_DEGR .GT. 0.0) THEN
C         Mach number from isentropic relation
          M2 = SQRT(2.0/(GAM2-1.0)*(TT_DEGR/TS_DEGR - 1.0))
          V2 = M2 * C2

        ELSE
C         Write warning and enter dummy values
C          WRITE(*,*) 'CHECK INPUTS TO REFPROP_STPROPS.FOR ROUTINE'
          V2 = 0.0
          M2 = 0.0

        END IF

C Static Temperature and Static Pressure at fan face
        IF (TS_DEGR .LT. 0.0) THEN  !TS is NOT measured
          TS2 = TT_DEGR / (1 + ((GAM2 - 1)/2.) * (M2**2))
        ELSE                         !TS is measured
          TS2 = TS_DEGR
        END IF

        IF (PS_PSI .LT. 0.0) THEN   !PS is NOT measured
          PS2 = PT_PSI*((1+((GAM2-1)/2.)*(M2**2))
     *           **((-GAM2)/(GAM2-1)))
        ELSE                         !PS is measured
          PS2 = PS_PSI
        END IF

C Partial Pressures of Air and Water Vapor
        PAP2 = PS2 * (1-XH2O)
        PHP2 = PS2 * XH2O

C Prepare REFPROP Inputs
        TPROP = TS2 / K2R
        PPROPA = PAP2 / KPA2PSI
        PPROPH = PHP2 / KPA2PSI

C Fan Inlet Density, Enthalpy and Gamma from REFPROP
C       For Air
        CALL PUREFLD(1)
        CALL TPRHO(TPROP, PPROPA, X, 2, 0, RHO, IERR, HERR)
        RHOA2 = RHO * MAIR * KGM2LBFT

        CALL THERM(TPROP, RHO, X, PPROPA, E, H, S, CV, CP, W, HJT)
        GAMA2 = CP / CV
        HA2 = H / MAIR  ! kJ/kg-K

C       For Water Vapor
        CALL PUREFLD(2)
        CALL TPRHO(TPROP, PPROPH, X, 2, 0, RHO, IERR, HERR)
        RHOH2 = RHO * MH2O * KGM2LBFT

        CALL THERM(TPROP, RHO, X, PPROPH, E, H, S, CV, CP, W, HJT)
        GAMH2 = CP / CV
        HH2 = H / MH2O  ! kJ/kg-K

C Density of the mixture
        RHO2 = RHOA2 + RHOH2

C Mass fraction of air and water vapor
        WAIR = RHOA2 / RHO2
        WH2O = RHOH2 / RHO2

C Average Molar Mass and gas constant of the Mixture
        MMIX = (( WAIR / MAIR ) + ( WH2O / MH2O ))**(-1)
        RMIX = R / MMIX

C Gamma of the mixture
        GAMNEW = (GAMA2 * WAIR) + (GAMH2 * WH2O)
        EGAM = ABS(GAM2 - GAMNEW)
        GAM2 = GAMNEW

C Enthalpy 
        H2 = ((HA2*WAIR) + (HH2*WH2O)) * JKGK2BLBR   ! BTU/lbm-R

C Speed of Sound of the Mixture
        C2 = SQRT(GAM2 * RMIX * GC * TS2)

        IF ( ICOUNT .GT. 50 ) THEN 
C           TYPE *,'REFPROP_FANPROPS...ICOUNT = ',ICOUNT
           RETURN
        ENDIF

      ENDDO

C Outputs after looping
      CTOT = C2
      HTOT = H2
      GAMTOT= GAM2
      RHOTOT = RHO2
      TSTOT = TS2
      PSTOT = PS2
      MTOT = SQRT(2.0/(GAM2-1.0)*(TT_DEGR/TS2 - 1.0))
      VTOT = MTOT * CTOT
      WH2OTOT = WH2O



      RETURN
      END
