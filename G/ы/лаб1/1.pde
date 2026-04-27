TITLE "Lab 1 - Variant 11 - Task 1 (Corrected)"
SELECT
  ERRLIM = 1e-4
COORDINATES
  CARTESIAN2
VARIABLES
  Temp
DEFINITIONS
  K_val       {Используем промежуточную переменную для чистоты}
  Q_val
  
  {Параметры 11 варианта}
  R_fuel = 0.008   
  R_shell = 0.010  
  T_gas = 300      
  alpha = 25000    
  
  K_fuel = 3.5
  K_shell = 18
  Q_source = 8e6

EQUATIONS
  DIV(K_val * grad(Temp)) + Q_val = 0

BOUNDARIES
  REGION 1 'System'
    {Сначала определяем общие параметры для внешней границы}
    K_val = K_shell
    Q_val = 0
    START(R_shell, 0)
    NATURAL(Temp) = alpha * (Temp - T_gas)
    ARC(CENTER=0,0) ANGLE=360

  REGION 2 'Fuel'
    {Затем переопределяем свойства только внутри этого региона}
    K_val = K_fuel
    Q_val = Q_source
    START(R_fuel, 0)
    ARC(CENTER=0,0) ANGLE=360

PLOTS
  CONTOUR(Temp)
  SURFACE(Temp)
  ELEVATION(Temp) FROM (0,0) TO (R_shell, 0)
END