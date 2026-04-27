TITLE "Lab 1 - Variant 11 - Task 3"
SELECT
  ERRLIM = 1e-4
COORDINATES
  CARTESIAN2
VARIABLES
  Temp
DEFINITIONS
  K_val
  source
  Rfuel = 0.008
  RShell = 0.010
  Tg = 300
  alfa = 25000
  
  Rt1 = 5e-4
  Rt2 = 1e-4
  {Используем условие для сектора}
  Rt_local = IF (x > 0 AND y > 0) THEN Rt1 ELSE Rt2 

EQUATIONS
  DIV(K_val * grad(Temp)) + source = 0

BOUNDARIES
  REGION 1 'Shell'
    K_val = 18
    source = 0
    START(RShell, 0)
    NATURAL(Temp) = alfa * (Temp - Tg)
    ARC(CENTER=0,0) ANGLE=360

  REGION 2 'Fuel'
    K_val = 3.5
    source = 8e6
    START(Rfuel, 0)
    CONTACT(Temp) = JUMP(Temp) / Rt_local
    ARC(CENTER=0,0) ANGLE=360

PLOTS
  CONTOUR(Temp)
  SURFACE(Temp)
  ELEVATION(Temp) FROM (0,0) TO (RShell, 0)
  ELEVATION(Temp) FROM (0,0) TO (0, RShell)
END