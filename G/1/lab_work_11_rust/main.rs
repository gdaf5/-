use std::fs::File;
use std::io::Write;

fn main() {
    // Parameters
    let l = 0.1;
    let t0 = 20.0;
    let alpha_diff = 1e-5;
    let lambda_cond = 50.0;
    let tg1 = 100.0;
    let alpha_g1 = 500.0;
    let tg2 = 20.0;
    let alpha_g2 = 100.0;
    
    let nx = 50;
    let nt = 50000;
    let dt = 0.0001;
    
    let dx = l / (nx as f64 - 1.0);
    
    // Stability check
    let fo = alpha_diff * dt / (dx * dx);
    if fo > 0.5 {
        println!("Warning: Stability condition violated (Fo={:.4} > 0.5).", fo);
    }
    
    // Initialize temperature array
    let mut t = vec![t0; nx];
    
    // Constants for boundary conditions
    let bi1 = alpha_g1 * dx / lambda_cond;
    let bi2 = alpha_g2 * dx / lambda_cond;
    
    // Time loop
    for n in 0..nt {
        let mut t_new = t.clone();
        
        // Interior nodes
        for i in 1..(nx - 1) {
            t_new[i] = t[i] + fo * (t[i+1] - 2.0 * t[i] + t[i-1]);
        }
        
        // Left boundary
        t_new[0] = t[0] + 2.0 * fo * (t[1] - t[0] + bi1 * (tg1 - t[0]));
        
        // Right boundary
        t_new[nx-1] = t[nx-1] + 2.0 * fo * (t[nx-2] - t[nx-1] + bi2 * (tg2 - t[nx-1]));
        
        t = t_new;
        
        // Output progress
        if n % 5000 == 0 {
            println!("Step {}: T_left={:.2}, T_mid={:.2}, T_right={:.2}", n, t[0], t[nx/2], t[nx-1]);
        }
    }
    
    // Save results
    let mut file = File::create("results_rust.txt").expect("Unable to create file");
    for temp in t {
        writeln!(file, "{}", temp).expect("Unable to write data");
    }
    println!("Results saved to results_rust.txt");
}
