C------------------------------------------------------------------------------
C  VCONEFLOW.FOR
C    Function subroutine to calculate mass flow across a V-cone.  This routine
C    for airflow is derived from the ISO 5167-5:2016 document.  REFPROP from
C    Nist is used to correct for humid air measurements.  This subroutine
C    is called from FACILITY_CALCS.tag
C
C  Modifications:
C  2018-01-04 - Initial version copied from FACILITY_CALCS.tag. (J. Borman)
C
C  Call: VCONEFLOW(PUPVC,DPVC,TVC,XH2O,D_PIPE,D_CONE,
C                  WVC,QVC,CDVC,VERR)
C
C  Inputs:
C    PUPVC   - Pressure upstream of V-Cone (psia)
C    DPVC    - DP across V-Cone (psid)
C    TVC     - Air Temperature at V-Cone (degR)
C    XH2O    - Mole Fraction of Water Vapor
C    D_PIPE	 - Diameter of the Pipe (inch)
C    D_CONE  - Max Diameter of the V-Cone (inch)
C
C  Outputs:
C    WVC     - Airflow Rate from V-Cone (lbm/s)
C    QVC     - Volumetric Flow Rate from V-Cone (ft^3/s)
C    CDVC    - Discharge Coefficient from V-Cone (dimless)
C    VERR    - Output error from VCONEFLOW
C------------------------------------------------------------------------------

      SUBROUTINE VCONEFLOW(PUPVC,DPVC,TVC,XH2O,D_PIPE,D_CONE,
     *            WVC,QVC,CDVC,VERR)

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

C  Set V-Cone Flow Conversions
      REAL U1/0.0360912/  !! psia/inH2O
      REAL U3/167.213/    !! lbm*ft/(s^2*inH2O)

C  Status Variables
      INTEGER VERR,ITER

C  Local Variables
      REAL PHP,PAP,MWAIR,RAIR,RHOA,GAMAIR,MWH2O,RH2O,RHOH,GAMH2O
      REAL RHOM,WAIR,WH2O,GAM,MW,RMIX,MU
      REAL BETA,Y,INVAR,CD,CD_OLD,XMASS,XMASS_OLD,RE,XMASS_ERR,CD_ERR

C  REFPROP inputs/outputs
      REAL*8 PPROP,TPROP,PPROPH,PPROPA,RHOPROP
      REAL*8 WMM,TTRP,TNBPT,TC,PC,DC,ZC,ACF,DIP,RGASRP
      REAL*8 RHOPA,RHOPH,E,H,S,CV,CP,W,HJT
      PARAMETER (NCMAX=20)   ! max number of components in mixture
      CHARACTER HRF*3, HERR*255
      CHARACTER*255 HF(NCMAX), HFMIX
      REAL*8 X(2)

C Air Composition (molar fractions)
      x(1) = 0.5000d0
      x(2) = 0.5000d0

C------------------------------------------------------------------------------
C  REFPROP Initialization
C------------------------------------------------------------------------------

C NOT NECESSARY TO CALL SETUP FROM THIS SUBROUTINE

C------------------------------------------------------------------------------
C  REFPROP Inputs
C------------------------------------------------------------------------------

      PPROP = PUPVC / KPA2PSI  !PPROP==PKPA,PINPA
      TPROP = TVC / K2R        !TPROP==TINK,TKA

C Partial Pressure of Water Vapor and Air
      PHP = XH2O * PUPVC
      PAP = (1 - XH2O) * PUPVC

      PPROPH = PHP/KPA2PSI
      PPROPA = PAP/KPA2PSI

C Air Properties
      CALL PUREFLD(1)
      CALL INFO(1,WMM,TTRP,TNBPT,TC,PC,DC,ZC,ACF,DIP,RGAS)
      MWAIR = WMM      ! Molecular Weight, g/mol
      RAIR = R / MWAIR ! Gas Constant, lbf*ft/(lbm*R*mol)

      CALL TPRHO(TPROP,PPROPA,X,0,0,RHOPA,IERR,HERR)
      RHOA = RHOPA * MWAIR * KGM2LBFT    ! Density, lb/ft^3

      RHOPROP = RHOA / (MWAIR*KGM2LBFT)
      CALL THERM(TPROP,RHOPROP,X,PPROPA,E,H,S,CV,CP,W,HJT)
      GAMAIR = CP / CV      ! Ratio of Specific Heats

C Water Vapor Properties
      CALL PUREFLD(2)
      CALL INFO(2,WMM,TTRP,TNBPT,TC,PC,DC,ZC,ACF,DIP,RGAS)
      MWH2O = WMM      ! Molecular Weight, g/mol
      RH2O = R / MWH2O ! Gas Constant, lbf*ft/(lbm*R*mol)

      CALL TPRHO(TPROP,PPROPH,X,2,0,RHOPH,IERR,HERR)
      RHOH = RHOPH * MWH2O * KGM2LBFT    ! Density, lb/ft^3

      RHOPROP = RHOH/(MH2O*KGM2LBFT)
      CALL THERM(TPROP,RHOPROP,X,PPROPH,E,H,S,CV,CP,W,HJT)
      GAMH2O = CP / CV      ! Ratio of Specific Heats

C Calculate the Mixture Properties
      RHOM = RHOA + RHOH    ! Combined Density
      WAIR = RHOA / RHOM    ! Dry Air Specific Humidity
      WH2O = RHOH / RHOM    ! Specific Humidity

      GAM = (GAMAIR*WAIR) + (GAMH2O*WH2O)
      MW = 1.0 / (WAIR/MWAIR + WH2O/MWH2O)
      RMIX = R / MW

C Call Viscosity Subroutine to Determine Mu
      CALL VISCMIX(PUPVC,TVC,XH2O,MU)

C------------------------------------------------------------------------------
C  V-Cone Airflow
C------------------------------------------------------------------------------

C The diameter ratio, BETA, is from ISO 5167-5:2016[eqn 2]
      BETA = SQRT(1. - (D_CONE/D_PIPE)**2)

C The expansibility factor of air, Y, is calculated based on
C  ISO 5167-5:2016[eqn 5]
      Y = 1.0 - (0.649 + .696 * BETA**4) * (DPVC) / (GAM*PUPVC)

C The invariant term of the airflow calculation, INVAR, does not change
C  with each iteration, ISO 5167-5:2016[eqn 1]
      INVAR = PI/48.0*(D_PIPE**2-D_CONE**2)*Y*
     *         SQRT(2.0*GC*DPVC*RHOM/(1.0 - BETA**4))
 
C Initalize iterative variables
      CD   = 1.0       !Start with a Cd guess of 1
      ITER = 0         !Iteration counter
      VERR = 0         !Convergence status
      XMASS_ERR = 1.0  !Compare massflow from last iteration

C Initial massflow guess, XMASS, from ISO 5167-5:2016[eqn 1]
      XMASS = CD * INVAR

C Start iteration for massflow convergence
      DO WHILE (XMASS_ERR .GT. 0.0001)

C     Reinitialize certain variables
        XMASS_OLD = XMASS
        CD_OLD = CD
        ITER = ITER + 1

C     Pipe Reynold's Number, RE, from ISO 5167-1:2003[3.2.2.1]
        RE = 4.0*XMASS / (PI * MU * D_PIPE)

C     Discharge Coefficient, CD, from "Calibration of a Cone Meter:
C      Report Number: 12RN-CE14259_2" applied to long radius piping
        CD = 1.901065E-21*RE**3 - 9.56826E-15*RE**2 + 1.586704E-8*RE
     *       + 0.7713142

C     Massflow of airflow past V-Cone, XMASS, from ISO 5167-5:2016[eqn 1]
         XMASS = CD * INVAR

C     Check XMASS and CD difference from last iteration
        XMASS_ERR = ABS(XMASS - XMASS_OLD)
        CD_ERR = ABS(CD - CD_OLD)

        IF (ITER .GT. 1000) THEN
          VERR = 1
          IF (DPVC .GT. 0.0) THEN
            WRITE(*,*), '****VCONE MASS FLOW NOT CONVERGED****'
          END IF
          EXIT
        END IF
      END DO

      WVC = XMASS
      QVC = XMASS / RHOM
      CDVC = CD

C------------------------------------------------------------------------------

      RETURN
      END
