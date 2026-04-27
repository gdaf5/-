import json
import numpy as np
import os

def solve_heat_equation(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)

    L = config['L']
    T0 = config['T0']
    a_diff = config['alpha_diff'] # Thermal diffusivity
    lam = config['lambda_cond']   # Thermal conductivity
    Tg1 = config['Tg1']
    alpha_g1 = config['alpha_g1']
    Tg2 = config['Tg2']
    alpha_g2 = config['alpha_g2']
    
    nx = config['nx']
    nt = config['nt']
    dt = config['dt']
    
    dx = L / (nx - 1)
    
    # Stability check
    Fo = a_diff * dt / (dx**2)
    if Fo > 0.5:
        print(f"Warning: Stability condition violated (Fo={Fo} > 0.5). Reduce dt.")
        return

    # Initialize temperature array
    T = np.full(nx, T0)
    
    # Precompute constants for boundary conditions
    # rho * cp = lam / a_diff
    # Boundary condition: alpha * (Tg - T) = lam * dT/dx
    # Explicit form for boundary: 
    # T_new[0] = T[0] + 2*Fo * (T[1] - T[0]) + 2*Fo*Bi*(Tg1 - T[0])
    # where Bi = alpha * dx / lam
    
    Bi1 = alpha_g1 * dx / lam
    Bi2 = alpha_g2 * dx / lam
    
    # Time loop
    for n in range(nt):
        T_new = T.copy()
        
        # Interior nodes
        for i in range(1, nx - 1):
            T_new[i] = T[i] + Fo * (T[i+1] - 2*T[i] + T[i-1])
            
        # Left boundary (convection)
        T_new[0] = T[0] + 2 * Fo * (T[1] - T[0] + Bi1 * (Tg1 - T[0]))
        
        # Right boundary (convection)
        T_new[nx-1] = T[nx-1] + 2 * Fo * (T[nx-2] - T[nx-1] + Bi2 * (Tg2 - T[nx-1]))
        
        T = T_new
        
        # Output progress
        if n % 500 == 0:
            print(f"Step {n}: T_left={T[0]:.2f}, T_mid={T[nx//2]:.2f}, T_right={T[nx-1]:.2f}")
            
    # Save results
    np.savetxt(os.path.join(os.path.dirname(__file__), "results.txt"), T)
    print("Results saved to results.txt")

if __name__ == "__main__":
    solve_heat_equation(os.path.join(os.path.dirname(__file__), "config.json"))
