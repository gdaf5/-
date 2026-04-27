import numpy as np
# from numba import jit # Убрали для совместимости
import time

# --- Параметры задачи ---
L = 0.02
lambda_ = 15.0
c = 500.0
rho = 7900.0
T0 = 300.0
alpha1, Tg1 = 2000.0, 20.0
alpha2, Tg2 = 500.0, 80.0

Nx = 50  # Увеличим разрешение
dx = L / (Nx - 1)
a = lambda_ / (c * rho)
dt = 0.5  # Шаг по времени можно сделать существенно больше!
Fo = a * dt / (dx**2)

# @jit(nopython=True) # Убрали для совместимости
def solve_step(T, Fo, Bi1, Bi2, Tg1, Tg2):
    """Решение методом прогонки (алгоритм Томаса) - неявная схема"""
    N = len(T)
    
    # Коэффициенты трехдиагональной матрицы
    A = np.zeros(N) # Нижняя диагональ
    B = np.zeros(N) # Главная диагональ
    C = np.zeros(N) # Верхняя диагональ
    D = np.zeros(N) # Правая часть
    
    # Граничное условие слева (3 род)
    B[0] = 1 + Fo * (1 + Bi1)
    C[0] = -Fo
    D[0] = T[0] + Fo * Bi1 * Tg1
    
    # Внутренние узлы
    for i in range(1, N - 1):
        A[i] = -Fo
        B[i] = 1 + 2 * Fo
        C[i] = -Fo
        D[i] = T[i]
        
    # Граничное условие справа (3 род)
    A[N-1] = -Fo
    B[N-1] = 1 + Fo * (1 + Bi2)
    D[N-1] = T[N-1] + Fo * Bi2 * Tg2
    
    # Прямой ход прогонки
    for i in range(1, N):
        m = A[i] / B[i-1]
        B[i] = B[i] - m * C[i-1]
        D[i] = D[i] - m * D[i-1]
        
    # Обратный ход
    T_new = np.zeros(N)
    T_new[N-1] = D[N-1] / B[N-1]
    for i in range(N-2, -1, -1):
        T_new[i] = (D[i] - C[i] * T_new[i+1]) / B[i]
        
    return T_new

# --- Инициализация ---
T = np.full(Nx, T0)
Bi1 = (alpha1 * dx) / lambda_
Bi2 = (alpha2 * dx) / lambda_

# --- Моделирование (Benchmark) ---
start_time = time.time()
for _ in range(200): # 200 шагов
    T = solve_step(T, Fo, Bi1, Bi2, Tg1, Tg2)
end_time = time.time()

print(f"Расчет завершен за {end_time - start_time:.4f} секунд.")
print("Температура (первые 10 узлов):", np.round(T[:10], 2))
